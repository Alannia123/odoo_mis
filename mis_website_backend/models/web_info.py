# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime, date
from random import randint


class WebAnouInfo(models.Model):
    _name = 'web.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=False, default='New')
    date = fields.Date('Date', default=lambda self: date.today())
    anounce = fields.Char('Annoucements')
    enable = fields.Boolean('Enable/Disable')
    color = fields.Char(string="Color HEX", default='#4d0000')



class BanInfo(models.Model):
    _name = 'banner.info'

    name = fields.Char('Name', required=False, default='New')
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())
    info = fields.Char('Annoucements')
    enable = fields.Boolean('Enable/Disable')
