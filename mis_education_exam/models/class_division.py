# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EducationClassDivision(models.Model):
    """
        Model representing Education Exams.

        This model stores information about education exams, including details like exam name,
        associated class, division, exam type, start and end dates, and related subjects.
    """
    _inherit = 'education.class.division'
    _description = 'Education Class Division'

    def get_all_class_students(self):
        academic_year_id = self.env['education.academic.year'].search([('enable', '=', True)], limit=1).id
        return academic_year_id