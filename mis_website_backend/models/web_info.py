# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint


class WebAnouInfo(models.Model):
    _name = 'web.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=False, default='New')
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())
    anounce = fields.Char('Annoucements')
    enable = fields.Boolean('Enable/Disable')



class BanInfo(models.Model):
    _name = 'banner.info'

    name = fields.Char('Name', required=False, default='New')
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())
    info = fields.Char('Annoucements')
    enable = fields.Boolean('Enable/Disable')
