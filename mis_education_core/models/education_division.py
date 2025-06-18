   # -*- coding: utf-8 -*-

from odoo import fields, models


class EducationDivision(models.Model):
    """Manages institution class divisions"""
    _name = 'education.division'
    _description = "Standard Division"

    name = fields.Char(string='Name', required=True,
                       help="Enter the Name of the Division")
    strength = fields.Integer(string='Class Strength',
                              help="Total strength of the class")
    faculty_id = fields.Many2one('education.faculty',
                                 string='Class Faculty',
                                 help="Class teacher/Faculty")
    class_id = fields.Many2one('education.class', string='Class',
                               help="Class of the division")
