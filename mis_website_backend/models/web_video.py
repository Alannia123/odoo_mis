# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime


class WebVideo(models.Model):
    _name = 'web.video'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', readonly=True,  default='New')
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    video = fields.Binary(string="Video")
    file_name = fields.Char('File Name')
    remarks = fields.Char('Remarks')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'name' not in vals or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('web.vide') or _('New')
        return super().create(vals_list)

