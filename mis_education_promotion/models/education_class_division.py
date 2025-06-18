# -*- coding: utf-8 -*-

from odoo import fields, models


class EducationClassDivision(models.Model):
    """ Inherits the model 'education.class.division' to add the fields. """
    _inherit = 'education.class.division'

    is_last_class = fields.Boolean(
        string="Is Last Class",
        help="Enable this option to set this class as last class")
    promote_class_id = fields.Many2one('education.class',
                                       string='Promotion Class',
                                       help='The promoted class for the student')
    promote_division_id = fields.Many2one('education.division',
                                          string='Promotion Division',
                                          help='The promoted division for '
                                               'the student')
    final_student_ids = fields.One2many('education.student.final.result',
                                        'division_id',
                                        string='Student Final Result',
                                        help='The student details for the '
                                             'final result.')
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the Academic "
             "Year without removing it.")
