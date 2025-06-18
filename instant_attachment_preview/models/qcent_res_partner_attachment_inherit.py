# -*- coding: utf-8 -*-
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments',help="Upload attachments for preview",)
