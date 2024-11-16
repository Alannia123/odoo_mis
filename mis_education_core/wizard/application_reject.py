# -*- coding: utf-8 -*-

from odoo import fields, models


class ApplicationReject(models.TransientModel):
    """This model for providing a rejection explanation while
            rejecting an application."""
    _name = 'application.reject'
    _description = 'Choose Reject Reason'

    reject_reason_id = fields.Many2one(
        'application.reject.reason',
        string="Reason",
        help="Select Reason for rejecting the Applications")

    def action_reject_reason_apply(self):
        """Write the reject reason of the application"""
        for rec in self:
            application = self.env['education.application'].browse(
                self.env.context.get('active_ids'))
            application.write({'reject_reason_id': rec.reject_reason_id.id})
            return application.reject_application()
