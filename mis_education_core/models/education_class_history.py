# -*- coding: utf-8 -*-

from odoo import fields, models


class EducationClassHistory(models.Model):
    """Used for managing student previous class details """
    _name = 'education.class.history'
    _description = "Class Room History"
    _rec_name = 'class_id'

    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Academic Year',
                                       help="Select the Academic Year")
    class_id = fields.Many2one('education.class.division',
                               string='Class', help="Select the class")
    student_id = fields.Many2one('education.student',
                                 string='Students',
                                 help="Select Student of class")
