# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EducationFaculty(models.Model):
    """Manages institution faculty details"""
    _name = 'education.faculty'
    _inherit = ['mail.thread']
    _description = 'Faculty Record'

    def action_create_employee(self):
        """Creating the employee for the faculty"""
        for rec in self:
            values = {
                'name': rec.name + rec.last_name,
                'gender': rec.gender,
                'birthday': rec.date_of_birth,
                'image_1920': rec.image,
                'work_phone': rec.phone,
                'work_email': rec.email,
            }
            emp_id = self.env['hr.employee'].create(values)
            rec.employee_id = emp_id.id

    @api.model
    def create(self, vals):
        """Overriding the create method to assign
        the sequence for newly creating records"""
        vals['faculty_id'] = self.env['ir.sequence'].next_by_code(
            'education.faculty')
        res = super(EducationFaculty, self).create(vals)
        return res

    name = fields.Char(string='Name', required=True,
                       help="Enter the first name")
    faculty_id = fields.Char(string="ID", readonly=True,
                             help="ID number of faculty")
    last_name = fields.Char(string='Last Name', help="Enter the last name")
    image = fields.Binary(string="Image", attachment=True,
                          help="Image of the faculty")
    email = fields.Char(string="Email",
                        help="Enter the Email for contact purpose")
    phone = fields.Char(string="Phone",
                        help="Enter the Phone for contact purpose")
    mobile = fields.Char(string="Mobile",
                         help="Enter the Mobile for contact purpose")
    date_of_birth = fields.Date(string="Date of Birth", help="Enter the DOB")
    guardian_name = fields.Char(string="Guardian", help="Your guardian is ")
    father_name = fields.Char(string="Father", help="Your Father name is ")
    mother_name = fields.Char(string="Mother", help="Your Mother name is ")
    subject_lines_ids = fields.Many2many('education.subject',
                                         string='Subject Lines',
                                         help="Subjects of faculty")
    employee_id = fields.Many2one('hr.employee',
                                  string="Related Employee",
                                  help="Related employee details")
    degree_id = fields.Many2one('hr.recruitment.degree',
                                string="Degree",
                                Help="Select your Highest degree")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender', required=True, default='male',
        help="Gender of the faculty", track_visibility='onchange')
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')], string='Blood Group',
        required=True, default='a+',
        track_visibility='onchange', help="Blood group og the faculty")
    user_id = fields.Many2one(
        'res.users',
        string='Related User',
        tracking=True,
        # domain="[('groups_id', 'in', [ref('base.group_user')])]"
    )
