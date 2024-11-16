# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    """Inheriting model 'account.move.line'"""
    _inherit = 'account.move.line'

    manual = fields.Boolean(string="Manual", help="True for manual",
                            default=True)
    date = fields.Date(string='Date', help="Date of payment", readonly=True)
    receipt_no = fields.Char(string='Receipt No',
                             help="Uniquely identifies the payment")

    @api.onchange('product_id')
    def _get_category_domain(self):
        """Set domain for invoice lines depend on selected category"""
        if self.move_id.fee_category_id:
            fee_types = self.env['education.fee.type'].search(
                [('category_id', '=', self.move_id.fee_category_id.id)])
            fee_list = []
            for fee in fee_types:
                fee_list.append(fee.product_variant_id.id)
            vals = {
                'domain': {
                    'product_id': [('id', 'in', tuple(fee_list))]
                }
            }
            return vals
