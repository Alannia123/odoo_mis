# -*- coding: utf-8 -*-

from odoo import fields, models


class EducationFeeCategory(models.Model):
    """Creating model 'education.fee.category' and adding fields"""
    _name = 'education.fee.category'
    _description = 'Education Fee Category'

    name = fields.Char(string='Name', required=True,
                       help='Create a fee category suitable for your '
                            'institution. Like Institutional, Hostel, '
                            'Transportation, Arts and Sports, etc')
    journal_id = fields.Many2one('account.journal',
                                 string='Journal', required=True,
                                 help='Setting up of unique journal for each '
                                      'category help to distinguish '
                                      'account entries of each category ')
    fee_structure = fields.Boolean(string='Have a Fee Structure?',
                                   required=True,
                                   help='If any fee structure want to be '
                                        'included in this category '
                                        'you must click here.'
                                        'For an example Institution '
                                        'category have different kind of'
                                        ' fee structures '
                                        'for different syllabuses')
