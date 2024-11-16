# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountJournal(models.Model):
    """Inherited 'account.journal' model"""
    _inherit = 'account.journal'

    is_fee = fields.Boolean(string='Is Educational fee?',
                            help="Whether educational fee or not.")

    def action_create_new_fee(self):
        """Function to return receipt form with details"""
        view = self.env.ref('mis_education_fee.receipt_form')
        context = self._context.copy()
        context.update({'journal_id': self.id, 'default_journal_id': self.id})
        context.update({'default_move_type': 'out_invoice'})
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': view.id,
            'context': context,
        }
