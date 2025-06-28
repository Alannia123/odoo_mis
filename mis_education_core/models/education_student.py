# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationStudent(models.Model):
    """For managing student records"""
    _name = 'education.student'
    _inherit = ['mail.thread']
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Student Record'

    def action_student_documents(self):
        """Return the documents student submitted
        along with the admission application"""
        self.ensure_one()
        if self.application_id.id:
            documents = self.env['education.document'].search(
                [('application_ref_id', '=', self.application_id.id)])
            documents_list = documents.mapped('id')
            return {
                'domain': [('id', 'in', documents_list)],
                'name': _('Documents'),
                'view_mode': 'tree,form',
                'res_model': 'education.document',
                'view_id': False,
                'context': {
                    'default_application_ref_id': self.application_id.id},
                'type': 'ir.actions.act_window'
            }

    def action_view_student_discipline_history(self):
        discipline_id = self.env['student.green.book'].search([('student_id', '=', self.id)])

        return {
            'name': _('Student Discipline'),
            'view_mode': 'form',
            'res_model': 'student.green.book',
            'res_id': discipline_id.id,
            'view_id': self.env.ref('mis_education_core.student_green_book_form').id,
            'type': 'ir.actions.act_window'
        }

    # @api.model
    # def name_search(self, name, args=None, operator='ilike', limit=100):
    #     if name:
    #         recs = self.search(
    #             [('name', operator, name)] + (args or []), limit=limit)
    #         if not recs:
    #             recs = self.search(
    #                 [('ad_no', operator, name)] + (args or []), limit=limit)
    #         return recs.name_get()
    #     return super(EducationStudent, self).name_search(
    #         name, args=args, operator=operator, limit=limit)
    #
    # @api.model
    # def create(self, vals):
    #     """Overriding the create method to assign
    #     sequence for the newly creating the record"""
    #     vals['ad_no'] = self.env['ir.sequence'].next_by_code(
    #         'education.student')
    #     res = super(EducationStudent, self).create(vals)
    #     return res

    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True,
        ondelete="cascade", help="Related partner of the student")
    last_name = fields.Char(string='Last Name', help="Enter last name")
    register_no = fields.Char('Registration Number', required=True)
    roll_no = fields.Char('Roll Number', required=True)

    date_of_birth = fields.Date(string="Date of Birth", required=True,
                                help="Enter date of birth of student")
    date_of_addmission = fields.Date(string="Date of Addmission", required=True,
                                help="Enter date of addmission of student")
    # guardian_id = fields.Many2one('res.partner', string="Guardian",
    #                               domain=[('is_parent', '=', True)],
    #                               help="Select guardian of the student")
    father_name = fields.Char(string="Father's Name", help="Father of the student")
    father_qualify = fields.Char(string="Father's Qualification", required=False)
    father_occupation = fields.Char(string="Father's Occupation", required=False)
    mother_name = fields.Char(string="Mother's Name", help="Mother of the student")
    mother_qualify = fields.Char(string="Mother's Qualification", required=False)
    mother_occupation = fields.Char(string="Mother's Occupation", required=False)
    mother_tongue = fields.Char('Mother Tongue')
    class_division_id = fields.Many2one('education.class.division',
                                        string="Class",
                                        help="Class of the student")
    admission_class_id = fields.Many2one('education.class',
                                         string="Class",
                                         help="Admission taken class")
    ad_no = fields.Char(string="Admission Number", readonly=True,
                        help="Admission number of student")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'),
                               ('other', 'Other')], string='Gender',
                              required=True, default='male',
                              track_visibility='onchange',
                              help="Gender details")
    blood_group = fields.Selection(
        [('none', 'None'),('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')],
        string='Blood Group', required=True, help="Blood group of student",
        default='none', track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Company',
                                 help="Current company")
    per_street = fields.Char(string="Street", help="Enter the street")
    per_street2 = fields.Char(string="Street2", help="Enter the street2")
    per_zip = fields.Char(change_default=True, string='ZIP code',
                          help="Enter the Zip Code")
    per_city = fields.Char(string='City', help="Enter the City name")
    per_state_id = fields.Many2one("res.country.state",
                                   string='State', ondelete='restrict',
                                   help="Select the State where you are from")
    per_country_id = fields.Many2one('res.country',
                                     string='Country', ondelete='restrict',
                                     help="Select the Country")
    medium_id = fields.Many2one('education.medium',
                                string="Medium", required=False,
                                help="Choose the Medium of class,"
                                     " like English, Hindi etc")
    sec_lang_id = fields.Many2one('education.subject',
                                  string="Second language",
                                  required=False,
                                  help="Choose the Second language",
                                  domain=[('is_language', '=', True)])
    mother_tongue = fields.Char(string="Mother Tongue", required=False,
                                domain=[('is_language', '=', True)],
                                help="Enter Student's Mother Tongue")
    caste = fields.Char(string="Caste", help="My Caste is ")
    religion = fields.Char(string="Religion", help="My Religion is ")
    is_same_address = fields.Boolean(string="Is same Address?",
                                     help="Tick the field if the Present and "
                                          "permanent address is same")
    application_id = fields.Many2one('education.application',
                                     string="Application No",
                                     help="Application number of student")
    class_history_ids = fields.One2many('education.class.history',
                                        'student_id',
                                        string="Class Details",
                                        help="Previous class history details")
    exist_sis_bro_info = fields.Boolean('Student has a sister/brother in this school(not cousin/relatives)')
    exist_name = fields.Char('Name')
    exist_name = fields.Char('Name')
    exist_class = fields.Many2one('education.class', 'Class')
    exist_section = fields.Many2one('education.division', 'Section')
    special_concern = fields.Char('Special Concern regarding Child')
    no_of_discipline_history = fields.Integer('Disp History', compute='_compute_no_of_discipline_history')
    aadhar_no = fields.Char('Aadhar Number', required=False)

    def _compute_no_of_discipline_history(self):
        for rec in self:
            discipline_id = self.env['student.green.book'].search([('student_id', '=', rec.id)])
            if discipline_id:
                rec.no_of_discipline_history = len(discipline_id.green_line_ids)
            else:
                rec.no_of_discipline_history = 0

    _sql_constraints = [
        ('register_no', 'unique(register_no)',
         "Another Student already exists with this register number!"),
    ]

    @api.onchange('class_division_id')
    def _onchange_class_division_id(self):
        """Method for checking the maximum number of students in a class"""
        for rec in self:
            if rec.class_division_id.actual_strength<len(rec.class_division_id.student_ids):
                raise ValidationError("The number of students exceeds the "
                                      "maximum strength of the class division.")
