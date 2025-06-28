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
    teacher_id = fields.Many2one('res.users', string='Uploaded by', default=lambda self: self.env.user)
    cover_photo = fields.Binary('Cover Photo')
    attachment_id = fields.Many2one('ir.attachment', 'Attachment',copy=False)
    state = fields.Selection([('draft', 'Draft'),('post', 'Posted'),('cancel', 'Cancel')], 'State', default='draft', tracking=True)


    def action_post(self):
        attachment = False
        attachment = self.env['ir.attachment'].create({
            'name': self.file_name,  # File name
            'type': 'binary',  # Must be binary for file storage
            'datas': self.pdf_file,  # Encode the file content
            'mimetype': 'application/pdf',  # MIME type
            'res_model': 'school.magazine',  # Attach it to a model (change 'your.model' to actual model name)
            'res_id': self.id,  # Attach it to a specific record
            'public': True,  # Attach it to a specific record
        })
        self.attachment_id = attachment.id

        self.write({'state' : 'post'})

    def action_cancel(self):
        self.write({'state' : 'cancel'})

    def action_rest_draft(self):
        self.write({'state' : 'draft'})