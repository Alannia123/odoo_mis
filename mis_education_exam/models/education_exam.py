# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EducationExam(models.Model):
    """
        Model representing Education Exams.

        This model stores information about education exams, including details like exam name,
        associated class, division, exam type, start and end dates, and related subjects.
    """
    _name = 'education.exam'
    _description = 'Education Exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _get_default_academic_year(self):
        academic_year_id = self.env['education.academic.year'].search([('enable', '=', True)], limit=1).id
        return academic_year_id

    name = fields.Char(
        string='Name', default='New', help='Name of the education exam.')
    class_id = fields.Many2one(
        'education.class', string='Class',
        help='Class associated with the exam.')
    division_id = fields.Many2one(
        'education.class.division', string='Division',
        help='Division associated with the exam.')
    exam_type_id = fields.Many2one(
        'education.exam.type', string='Type', required=True,
        help='Type of the education exam.')
    school_class_division_wise = fields.Selection(
        [('school', 'School'), ('class', 'Class'), ('division', 'Division')],
        related='exam_type_id.school_class_division_wise',
        string='School/Class/Division Wise',
        help='Specifies whether the exam is school, class, or division-wise.')
    class_division_hider = fields.Char(
        string='Class Division Hider',
        help='Hider field for class and division.')
    # start_date = fields.Date(
    #     string='Start Date', required=True,
    #     help='Start date of the education exam.')
    # end_date = fields.Date(
    #     string='End Date', required=True,
    #     help='End date of the education exam.')
    subject_line_ids = fields.One2many(
        'education.subject.line', 'exam_id',
        string='Subjects', help='Subjects associated with the exam.')
    sylabus_line_ids = fields.One2many(
        'exam.syllabus', 'exam_id',
        string='Syllabus', help='Syllabus associated with the exam.')
    state = fields.Selection(
        [('draft', 'Draft'), ('waiting_syllabus', 'Waiting For Syllabus'), ('ongoing', 'Ongoing'),
         ('close', 'Closed'), ('cancel', 'Canceled')],
        default='draft', help='Current state of the education exam.')
    academic_year_id = fields.Many2one(
        'education.academic.year', string='Academic Year', readonly=True, required=True, default=_get_default_academic_year,
        help='Academic year associated with the division.')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(), readonly=True,
        help='Company associated with the exam.')

    def get_all_class_divs(self):
        all_class_ids = self.env['education.class.division'].search([('class_id', '=', self.class_id.id)])
        return  all_class_ids

    # Create subjects on class onchange
    @api.onchange('class_id')
    def onchange_add_sale_bom_comp(self):
        subject_line_data = []
        syllabus_line_data = []
        if self.class_id:
            # Load Subjects on Exam Subjects
            if self.subject_line_ids:
                self.subject_line_ids = [fields.Command.clear()]
            subject_line_data = [fields.Command.clear()]
            for subject in self.class_id.subject_ids:
                subject_line_data = [fields.Command.create({
                                                        'subject_id': subject.subject_id.id,
                                                    })]
                self.subject_line_ids = subject_line_data

            # Load Subjects on Syllabus
            if self.sylabus_line_ids:
                self.sylabus_line_ids = [fields.Command.clear()]
            syllabus_line_data = [fields.Command.clear()]
            for subject in self.class_id.subject_ids:
                syllabus_line_data = [fields.Command.create({
                                                        'subject_id': subject.subject_id.id,
                                                    })]
                self.sylabus_line_ids = syllabus_line_data


    # @api.model
    # def create(self, vals):
    #     """
    #         Create method for Education Exam.
    #     """
    #     res = super(EducationExam, self).create(vals)
    #     if res.division_id:
    #         res.class_id = res.division_id.class_id.id
    #     return res

    @api.onchange('class_division_hider')
    def _onchange_class_division_hider(self):
        """
            Onchange method for Class Division Hider.

            Updates the school_class_division_wise field based on the
             class_division_hider value.
        """
        self.school_class_division_wise = 'school'


    def action_close_exam(self):
        """
            Sets the state of the exam to 'close'.
        """
        self.state = 'close'

    def action_cancel_exam(self):
        """
            Sets the state of the exam to 'cancel'.
        """
        self.state = 'cancel'

    def action_confirm_exam(self):
        """
            Confirm the exam.

            Validates the exam, sets the name based on exam type, start date, and division/class,
            and sets the state to 'ongoing'.

            :raises: UserError if no subjects are added.
        """
        for syl in self.sylabus_line_ids:
            if not syl.attachment:
                raise ValidationError(_('Syllabus not yet added on %s', syl.subject_id.name))
        self.state = 'ongoing'


    def send_notify_to_teachers(self):
        print('gfghfgfg')
        class_divisions = self.env['education.class.division'].search([('class_id', '=', self.class_id.id)])
        print('CDLLLLLLLLLLLLLL',class_divisions)
        self.name = self.exam_type_id.name + '-' + self.academic_year_id.name
        for cl in class_divisions:
            teacher_id = cl.faculty_id.employee_id.user_id
            self.activity_schedule('mis_education_exam.syllabus_entry_teachers_notification',
                                             user_id=teacher_id.id,
                                             note=f'{self.name} Exam Announced and please enter your Syllabus')
        message_string = ''
        message_string = 'hello odoo whatsapp'
        self.state = 'waiting_syllabus'

        # user = self.env.user
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': "https://api.whatsapp.com/send?phone=" +
        #            user.partner_id.mobile + "&text=" + message_string,
        #     'target': 'new',
        #     'res_id': self.id,
        # }





        # activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id),
        #                                                 ('activity_type_id', '=', self.env.ref(
        #                                                     'grinn_purchase.send_notification_purchase_order_manager_approval_activity').id)])
        # activity_id.action_feedback(feedback='Approved')
        # other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id),
        #                                                        ('activity_type_id', '=', self.env.ref(
        #                                                            'grinn_purchase.send_notification_purchase_order_manager_approval_activity').id)])
        # other_activity_ids.unlink()
        # users = self.env.ref('purchase.group_purchase_manager').users



class EducationSubjectLine(models.Model):
    """
        Model representing Education Subject Line.
        This model stores information about subjects associated with an education exam, including
        details like subject, date, time, marks, associated exam, and company.
    """

    _name = 'education.subject.line'
    _description = 'Subject Line'

    subject_id = fields.Many2one(
        'education.subject', string='Subject', readonly=True,
        help='Subject associated with the subject line.')
    date = fields.Date(
        string='Date', required=False,
        help='Date of the subject line.')
    time_from = fields.Float(
        string='Time From', required=True, help='Start time of the subject.')
    time_to = fields.Float(
        string='Time To', required=True, help='End time of the subject.')
    mark = fields.Integer(
        string='Mark', help='Mark associated with the subject.')
    exam_id = fields.Many2one(
        'education.exam', string='Exam',
        help='Exam associated with the subject line.')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help='Company associated with the subject line.')

    @api.onchange('date')
    def _check_exam_date(self):
        for record in self:
            """Method for validating the exam date"""
            today_date = fields.Date.today()
            if (record.date < today_date):
                raise ValidationError(
                    'The exam date must be today or future dates of the exam.')

    @api.constrains('exam_date', 'time_from', 'time_to', 'exam_id')
    def _check_time_overlap(self):
        """Method for checking date and time overlapping"""
        for record in self:
            overlapping_records = self.search([
                ('exam_id', '=', record.exam_id.id),
                ('date', '=', record.date),
                ('id', '!=', record.id),
                '|',
                '&', ('time_from', '<', record.time_to),
                ('time_to', '>', record.time_from),
                '&', ('time_from', '<', record.time_to),
                ('time_to', '>', record.time_from)
            ])
            if overlapping_records:
                raise ValidationError(
                    'The subject exam times cannot overlap with another '
                    'subject on the same date.')



class ExamSylabus(models.Model):
    _name = 'exam.syllabus'
    _description = 'Exam Syllabus'

    subject_id = fields.Many2one(
        'education.subject', string='Subject', readonly=False,
        help='Subject associated with the subject line.')
    attachment = fields.Binary(string='Attachment')
    file_name = fields.Char('File Name')
    exam_id = fields.Many2one(
        'education.exam', string='Exam',
        help='Exam associated with the subject line.')


class EducationExamType(models.Model):
    """
        Model representing Education Exam Type.

        This model stores information about different types of education exams, including
        details like the name of the exam type, whether it's school, class, division-wise,
        or a final exam that promotes students to the next class.
    """

    _name = 'education.exam.type'
    _description = 'Education Exam Type'

    name = fields.Char(
        string='Name', required=True, help='Name of the education exam type.')
    school_class_division_wise = fields.Selection(
        [('school', 'School'), ('class', 'Class'), ('division', 'Division'),
         ('final',
          'Final Exam (Exam that promotes students to the next class)')],
        string='Exam Type', default='class', help='Type of education exam.', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help='Company associated with the education exam type.')
