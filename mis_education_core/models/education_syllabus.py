# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationSyllabus(models.Model):
    """Manages syllabus of every subjects"""
    _name = 'education.syllabus'
    _description = 'Syllabus Details'

    name = fields.Char('Name', required=True, help="Name of the syllabus")
    class_id = fields.Many2one('education.class', string='Class',
                               help="Enter the class for syllabus")
    subject_id = fields.Many2one('education.subject',
                                 string='Subject', help="Select subjects")
    total_hours = fields.Float(string='Total Hours',
                               help="Total hours need for the subject")
    description = fields.Text(string='Syllabus Modules',
                              help="Note about the syllabus")

    @api.constrains('total_hours')
    def validate_time(self):
        """Returns validation error if the hours is not a positive value"""
        for rec in self:
            if rec.total_hours <= 0:
                raise ValidationError(_('Hours must be greater than Zero'))
