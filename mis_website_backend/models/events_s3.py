# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint
import boto3


class ProgramEvents(models.Model):
    _name = 'program.events'

    name = fields.Char('Name', required=True)
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())

class ProgramEventsGalleryAws(models.Model):
    _name = 'program.gallery.aws'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'event_id'

    name = fields.Char('Name', readonly=True)
    date = fields.Date('Date',default=lambda self: fields.Datetime.now(), readonly=True)
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    event_id = fields.Many2one('program.events', 'Event', required=True)
    # photo_ids = fields.One2many('ir.gallery.photo','gallery_id', 'Photos')
    remarks = fields.Char('Remarks')
    attach_count = fields.Integer('Photos', compute='count_photos')
    aws_url_ids = fields.One2many('program.gallery.aws.url', 'program_id', 'Urls')
    s3_image_html = fields.Html(string="Photos", readonly=True, compute='_compute_s3_image_html')

    def _compute_s3_image_html(self):
        for rec in self:

            html = ''
            if rec.aws_url_ids:
                for index, img in enumerate(rec.aws_url_ids, start=1):
                    if img.url:
                        html += f'''
                                    <div style="margin-bottom:10px;">
                                        <span style="
                                            background-color: red;
                                            color: white;
                                            padding: 2px 8px;
                                            border-radius: 10px;
                                            font-size: 12px;
                                            margin-right: 10px;
                                            display: inline-block;
                                        ">
                                            {index}
                                        </span>
                                        <img src="{img.url}" width="200" style="vertical-align: middle;"/>
                                    </div>
                                '''
            rec.s3_image_html = html


    def count_photos(self):
        for rec in self:
            rec.attach_count = len(rec.aws_url_ids)


    def view_and_add_attachments(self):
        self.ensure_one()
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'program.gallery'), ('res_id', '=', self.id)])
        return {
            'name': _('View photos'),
            'view_mode': 'kanban,tree,form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            # 'context': {'default_gallery_id': self.id},
            'domain': [('id', 'in', photo_attaches.ids)],
            'target': 'current',
        }


    def get_random_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'program.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches[:4])
            return photo_attaches[:4]

    def get_current_enevt_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'program.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            return photo_attaches

    def write(self, vals_list):
        res = super(ProgramEventsGalleryAws, self).write(vals_list)
        self._compute_s3_image_html()
        return res




class ProgramEventsGalleryAwsurl(models.Model):
    _name = 'program.gallery.aws.url'


    program_id = fields.Many2one('program.gallery.aws', 'Program Id')
    sr_no = fields.Integer('Sr.No')
    url = fields.Char('Url')

    # def unlink(self):
    #     res = super(ProgramEventsGalleryAwsurl, self).unlink()
    #
    #     # Initialize the S3 client
    #     s3 = boto3.client('s3')
    #
    #     # Set your bucket name and file name (key)
    #     bucket_name = 'misodoo'
    #     print('selffffffffffffff',self)
    #     file_name = 'folder/subfolder/yourfile.jpg'  # S3 object key
    #
    #     # Delete the object
    #     response = s3.delete_object(Bucket=bucket_name, Key=file_name)
    #
    #     # Optional: check response
    #     print("Deleted:", response)
    #
    #     etdfhdh
    #     self._compute_s3_image_html()
    #     return res


class EventsGallery(models.Model):
    _name = 'event.gallery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'event_id'

    name = fields.Char('Name', readonly=True)
    date = fields.Date('Date',default=lambda self: fields.Datetime.now(), readonly=False)
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    event_id = fields.Many2one('program.events', 'Event', required=True)
    # photo_ids = fields.One2many('ir.gallery.photo','gallery_id', 'Photos')
    remarks = fields.Char('Remarks')
    attach_count = fields.Integer('Photos', compute='count_photos')


    def count_photos(self):
        for rec in self:
            rec.attach_count = self.env['ir.attachment'].search_count([('res_model', '=', 'event.gallery'), ('res_id', '=', rec.id)])


    def view_and_add_attachments(self):
        self.ensure_one()
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'event.gallery'), ('res_id', '=', self.id)])
        return {
            'name': _('View photos'),
            'view_mode': 'kanban,tree,form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            # 'context': {'default_gallery_id': self.id},
            'domain': [('id', 'in', photo_attaches.ids)],
            'target': 'current',
        }


    def get_random_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'event.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches[:4])
            return photo_attaches[:4]

    def get_current_enevt_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'event.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            return photo_attaches

