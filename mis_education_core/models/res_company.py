# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    """Inheriting res_company for adding field related to an
        education institution"""
    _inherit = 'res.company'

    affiliation = fields.Char(string='Affiliation', help="Affiliation details")
    register_num = fields.Char(string='Register', help="Registration details")
    base_class_id = fields.Many2one('education.class',
                                    string="Lower class",
                                    help="Smallest class of institute")
    higher_class_id = fields.Many2one('education.class',
                                      string="Higher class",
                                      help="Highest class of institute")
