# -*- coding: utf-8 -*-

from odoo import fields, models, api


class EducationClass(models.Model):
    """For managing classes"""
    _name = 'education.class'
    _description = "Standard"

    name = fields.Char(string='Name', required=True,
                       help="Enter the Name of the Class")
    type = fields.Selection([('lkg', 'LKG'),('ukg', 'UKG'), ('onetwo', '1-2 STD'), ('threefive', '3-5 STD'),
                                    ('sixeight', '6-8 STD'), ('ninten', '9-10 STD')],
                            'Report Card', required=False)
    subject_ids = fields.One2many('education.class.subject',
                                   'class_id',
                                   string="Syllabus",
                                   help="Syllabus of the class")
    # division_ids = fields.One2many('education.division',
    #                                'class_id',
    #                                string="Division",
    #                                help="Divisions of class")
    open_addmission = fields.Boolean('Open For Addmission?')
    seats_available = fields.Integer('Available Seats')
    filled_seats = fields.Integer('Filled Seats')


    @api.onchange('seats_available')
    def onchage_addmision_open(self):
        if  self.seats_available != 0 and self.seats_available > self.filled_seats:
            self.open_addmission = True
        else:
            self.open_addmission = False



    def get_filled_seats_on_class(self):
        admision_open_classes = self.env['education.class'].search([('open_addmission', '=', True)])
        academic_year = self.env['education.academic.year'].search([('next_acdemic_year', '=', True)])
        for ad_class in admision_open_classes:
            print('CALSSSSSSSSSSSSSSSSSSSSSSS',self)
            print('CALSSSSSSSSSSSSSSSSSSSSSSS',ad_class)
            stu_applications = self.env['education.application'].search([('academic_year_id', '=', academic_year.id),
                                                                     ('admission_class_id', '=', ad_class.id)])
            filled_seats = len(stu_applications)
            print('SSSSSSSSSSSSSSSSS',stu_applications)
            ad_class.filled_seats = filled_seats
            if ad_class.filled_seats >= ad_class.seats_available:
                ad_class.open_addmission = False







class EducationClassSubjects(models.Model):
    """For managing classes"""
    _name = 'education.class.subject'
    _description = "Subjects"

    class_id = fields.Many2one('education.class', 'Class')
    type = fields.Selection(related='class_id.type', string=
                            'Report Card', required=True)
    subject_id = fields.Many2one('education.subject', 'Subject', required=True, domain="[('type', '=', type)]")
    faculty_ids = fields.Many2many('education.faculty', 'Faculties',required=True)

