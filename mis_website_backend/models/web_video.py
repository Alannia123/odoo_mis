# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
import boto3
import base64
import logging
from odoo import models, fields
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class WebVideo(models.Model):
    _name = 'web.video'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', readonly=True,  default='New')
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    video = fields.Binary(string="Video")
    file_name = fields.Char('File Name')
    remarks = fields.Char('Remarks')
    s3_url = fields.Char(string="S3 URL", readonly=True)
    show_website = fields.Boolean('Show On Website')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'name' not in vals or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('web.vide') or _('New')
        return super().create(vals_list)

    def upload_image_to_s3(self):
        # AWS S3 credentials
        aws_access_key = self.env['ir.config_parameter'].sudo().get_param('mis_website_backend.amazon_access_key')
        aws_secret_key = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_secret_key')
        aws_bucket_name = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_bucket_name')
        aws_region_name = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_region_name')
        print('WSEFFFFFFFFFFFFF',aws_access_key)
        if not aws_access_key:
            raise ValidationError(_("Please Add AWS Access Key"))
        if not aws_secret_key:
            raise ValidationError(_("Please Add AWS Secret Key"))
        if not aws_bucket_name:
            raise ValidationError(_("Please Add AWS Bucket Name"))
        if not aws_region_name:
            raise ValidationError(_("Please Add AWS Region Name"))
        for rec in self:
            if not rec.video:
                continue

            session = boto3.session.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region_name,
            )
            s3 = session.resource('s3')

            file_name = rec.file_name
            # file_content = base64.b64decode(datas[1])
            file_data = base64.b64decode(rec.video)

            try:
                s3.Bucket(aws_bucket_name).put_object(
                    Key=file_name,
                    Body=file_data,
                    ContentType='video/mp4',
                    ACL='public-read'  # Or 'private'
                )
                s3_url = f"https://{aws_bucket_name}.s3.{aws_bucket_name}.amazonaws.com/{file_name}"
                rec.write({'s3_url': s3_url})
                _logger.info(f"Uploaded image to S3: {s3_url}")
            except Exception as e:
                _logger.error(f"Error uploading to S3: {str(e)}")

