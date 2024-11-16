# -*- coding: utf-8 -*-

from odoo import fields, models


class ApplicationRejectReason(models.Model):
    """Used for managing reject reasons of applications"""
    _name = 'application.reject.reason'
    _description = 'Reject ReasonS'

    name = fields.Char(string="Reason", required=True,
                       help="Possible Reason for rejecting the Applications")
