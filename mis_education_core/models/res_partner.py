# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Inherited model for adding two fields to determine
                        whether the partner student or parent"""
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Is a Student",
                                help="Enable if the partner is a student")
    is_teacher = fields.Boolean(string="Is a Teacher",
                               help="Enable if the partner is a teacher")
