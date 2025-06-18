# -*- coding: utf-8 -*-

from odoo import fields, models


class StandardMedium(models.Model):
    """Manages student class medium details"""
    _name = "education.medium"
    _description = "Standard Medium"

    name = fields.Char(string='Name', required=True,
                       help="Enter the Name of the Medium")
    code = fields.Char(string='Code', help="Enter the Medium Code")
    description = fields.Text(string='Description', help="Note about medium")
