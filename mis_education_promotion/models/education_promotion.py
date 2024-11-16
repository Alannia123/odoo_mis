from dateutil import relativedelta
from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError


class EducationPromotion(models.Model):
    """ Model to manage academic promotions. """
    _name = 'education.promotion'
    _description = 'Promotion'

    name = fields.Many2one('education.academic.year',
                           string="Academic Year", required=True,
                           help='Represents the academic year for which '
                                'promotion details are recorded.')
    academic_result_ids = fields.One2many(
        'education.student.final.result',
        'closing_id', string="Results",
        help='Stores the final results of students associated with '
             'this promotion.')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('result_computed', 'Result Computed'),
         ('close', 'Closed')], default='draft', string='State',
        help='The states of the promotion')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help='Specifies the company associated with the academic promotion.')

    def action_compute_final_result(self):
        """
            Compute and record final results based on exam outcomes.
            This method sets the state of the academic promotion to 'result_computed'.
            It retrieves exam results related to the academic year and updates the
            education.student.final.result records accordingly.
            Returns:
                None
            """
        self.state = 'result_computed'
        exam_result_env = self.env['education.exam.results']
        if not exam_result_env.search([
            ('academic_year_id', '=', self.name.id)]).filtered(
            lambda l: l.exam_id.exam_type_id.school_class_division_wise == 'final'):
            raise ValidationError(
                'No Final Result found for the Academic Year %s' % self.name.id)
        for i in exam_result_env.search([
            ('academic_year_id', '=', self.name.id)]).filtered(
            lambda l: l.exam_id.exam_type_id.school_class_division_wise == 'final'):
            self.env['education.student.final.result'].create({
                'student_id': i.student_id.id,
                'final_result': 'pass' if i.overall_pass else 'fail',
                'division_id': i.division_id.id,
                'academic_year_id': i.division_id.academic_year_id.id,
                'closing_id': self.id,
            })

    def close_academic_year(self):
        """
            Close the current academic year and initiate the process of
            transitioning to a new academic year.
            This method sets the state of the academic promotion to 'close' and
             performs the following actions:
            1. Creates a new academic year for the subsequent year.
            2. Copies class divisions from the current academic year to the
            new academic year.
            3. Generates promotion classes for non-last classes in the new
            academic year.
            4. Promotes or retains students based on their final results.
            Returns:
                None
            Raises:
                UserError: Raised if no promotion class is set for a class with
                missing promotion details.
            """
        self.state = 'close'
        division_obj = self.env['education.class.division']
        new_academic_year = self.env['education.academic.year'].create(
            {'name': str(
                fields.Date.from_string(
                    self.name.ay_end_date).year) + "-" + str(
                fields.Date.from_string(self.name.ay_end_date).year + 1),
             'sequence': self.name.sequence + 1,
             'ay_start_date': self.name.ay_end_date,
             'ay_end_date': str(
                 fields.Date.from_string(self.name.ay_end_date) +
                 relativedelta.relativedelta(months=+12))[:10],
             })
        for div in division_obj.search(
                [('academic_year_id', '=', self.name.id)]):
            if not div.is_last_class:
                if not div.promote_class_id or not div.promote_division_id:
                    raise ValidationError(
                        'Promotion Class or Promotion Division is not added '
                        'for the class %s - %s'
                        % (div.class_id.name, div.division_id.name))
            new_division = division_obj.create({
                'actual_strength': div.actual_strength,
                'academic_year_id': new_academic_year.id,
                'class_id': div.class_id.id,
                'faculty_id': div.faculty_id.id,
                'division_id': div.division_id.id,
                'is_last_class': div.is_last_class,
            })
            if not new_division.is_last_class:
                new_division.sudo().write({
                    'promote_division_id': div.promote_division_id,
                    'promote_class_id': div.promote_class_id,
                })
        for new_div in division_obj.search(
                [('academic_year_id', '=', new_academic_year.id),
                 ('is_last_class', '=', False)]):
            promote = division_obj.search(
                [('academic_year_id', '=', new_academic_year.id),
                 ('name', '=', str(new_div.promote_class_id.name) + "-" + str(
                     new_div.promote_division_id.name))])
            if not promote:
                division_obj.create({
                    'actual_strength': new_div.actual_strength,
                    'academic_year_id': new_academic_year.id,
                    'class_id': new_div.promote_class_id.id,
                    'division_id': new_div.promote_division_id.id,
                    'faculty_id': new_div.faculty_id.id,
                })
        for div in division_obj.search(
                [('academic_year_id', '=', self.name.id)]):
            current_class = division_obj.search([
                ('name', '=', div.name),
                ('academic_year_id', '=', new_academic_year.id)], limit=1)
            if div.is_last_class:
                promotion_class = False
            else:
                if div.promote_class_id and div.promote_division_id:
                    promotion_class = division_obj.search([
                        ('name', '=',
                         div.promote_class_id.name + "-" + div.promote_division_id.name),
                        ('academic_year_id', '=', new_academic_year.id)],
                        limit=1)
                else:
                    raise UserError(_(
                        'There is no promotion class is set for the class %s.'
                        '\nIf it is the last class, Please mark the Check box '
                        'in the Class Division', div.name))
            for student in div.final_student_ids:
                if student.final_result == 'pass':
                    if not promotion_class:
                        student.student_id.active = False
                    else:
                        student.student_id.class_division_id = promotion_class.id
                elif student.final_result == 'fail':
                    student.student_id.class_division_id = current_class.id
