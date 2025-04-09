# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint
import boto3


class WebSlide(models.Model):
    _name = 'web.slide.image'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', readonly=False, required=True)
    date = fields.Date('Date',default=lambda self: fields.Datetime.now(), readonly=True)
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    # attach_count = fields.Integer('Photos', compute='count_photos')
    image_url_ids = fields.One2many('web.slide.image.url', 'slide_id', 'Urls')
    # s3_image_html = fields.Html(string="Photos", readonly=True, compute='_compute_s3_image_html')
    enable = fields.Boolean('Enable')

    # def _compute_s3_image_html(self):
    #     for rec in self:
    #         html = ''
    #         if rec.image_url_ids:
    #             for index, img in enumerate(rec.image_url_ids, start=1):
    #                 if img.url:
    #                     html += f'''
    #                                 <div style="margin-bottom:10px;">
    #                                     <span style="
    #                                         background-color: red;
    #                                         color: white;
    #                                         padding: 2px 8px;
    #                                         border-radius: 10px;
    #                                         font-size: 12px;
    #                                         margin-right: 10px;
    #                                         display: inline-block;
    #                                     ">
    #                                         {index}
    #                                     </span>
    #                                     <img src="{img.url}" width="200" style="vertical-align: middle;"/>
    #                                 </div>
    #                             '''
    #         rec.s3_image_html = html


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
    #
    # def write(self, vals_list):
    #     res = super(WebSlide, self).write(vals_list)
    #     # self._compute_s3_image_html()
    #     return res

class WebSlideUrl(models.Model):
    _name = 'web.slide.image.url'


    slide_id = fields.Many2one('web.slide.image', 'Slide')
    sr_no = fields.Integer('Sr.No')
    url = fields.Char('Url')
    image_preview = fields.Html(string="Preview", compute="_compute_image_preview", sanitize=False)

    @api.depends('url')
    def _compute_image_preview(self):
        sr_no = 1
        for rec in self:
            rec.image_preview = f'<img src="{rec.url}" width="100"/>'
            rec.sr_no = sr_no
            sr_no += 1

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


