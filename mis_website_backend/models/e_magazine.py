# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint




class SchoolMagazine(models.Model):
    _name = 'school.magazine'
    _description = 'School e-Magazine'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(string='Magazine Title', required=True)
    upload_date = fields.Date(string='Upload Date', default=fields.Date.today)
    file_name = fields.Char(string='PDF File', required=True, attachment=True)
    pdf_file = fields.Binary(string='PDF File', required=True, attachment=True)
    # division_id = fields.Many2one('education.class.division', 'Division')
    teacher_id = fields.Many2one('res.users', string='Uploaded by', default=lambda self: self.env.user)
    cover_photo = fields.Binary('Cover Photo')
    state = fields.Selection([('draft', 'Draft'),('post', 'post')], 'State', default='draft', tracking=True)


    def action_post(self):
        self.write({'state' : 'post'})