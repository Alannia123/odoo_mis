# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMove(models.Model):
    """The Dashboard model used to build the all details of the
    Educational system"""
    _name = "erp.dashboard"
    _description = "Education ERP Dashboard"