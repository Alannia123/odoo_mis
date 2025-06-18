# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Akhil Ashok @cybrosys(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, models, _
import os ,base64 , io
import gzip
import boto3
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError, ValidationError


class UploadMultiDocuments(models.Model):
    _name = "upload.multi.documents"
    _description = "Upload Multiple Documents"

    @api.model
    def document_file_create(self, value, name, selected_ids, model):
        if selected_ids:
            data = value.split('base64')[1] if value else False
            for rec_id in selected_ids:
                event_id = self.env['program.gallery.aws'].browse(rec_id)
                # AWS S3 credentials
                AWS_ACCESS_KEY = self.env['ir.config_parameter'].sudo().get_param(
                    'mis_website_backend.amazon_access_key')
                # AWS_ACCESS_KEY = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_access_key')
                AWS_SECRET_KEY = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_secret_key')
                BUCKET_NAME = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_bucket_name')
                REGION = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_region_name')
                print('WSEFFFFFFFFFFFFF', AWS_ACCESS_KEY)
                if not AWS_ACCESS_KEY:
                    raise ValidationError(_("Please Add AWS Access Key"))
                if not AWS_SECRET_KEY:
                    raise ValidationError(_("Please Add AWS Secret Key"))
                if not BUCKET_NAME:
                    raise ValidationError(_("Please Add AWS Bucket Name"))
                if not REGION:
                    raise ValidationError(_("Please Add AWS Region Name"))
                session = boto3.session.Session(
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                    region_name=REGION,
                )
                s3 = session.resource('s3')

                file_name = name
                # file_content = base64.b64decode(datas[1])
                file_data = base64.b64decode(data)

                try:
                    s3.Bucket(BUCKET_NAME).put_object(
                        Key=file_name,
                        Body=file_data,
                        ContentType='image/jpg',
                        ACL='public-read'  # Or 'private'
                    )
                    s3_url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file_name}"
                    url_id = self.env['program.gallery.aws.url'].create({
                                                                        'program_id' : event_id.id,
                                                                        # 'sr_no' : sr_no,
                                                                        'url' : s3_url,
                                                                    })
                    print("Uploaded image to S3: ", s3_url)
                except Exception as e:
                    _logger.error(f"Error uploading to S3: {str(e)}")
            # self.env['ir.attachment'].create({
            #         'name': name,
            #         'datas': data,
            #         'res_model': model,
            #         'res_id': rec_id,
            #     })
            return True

class UploadSlideImage(models.Model):
    _name = "slide.multi.documents"
    _description = "Upload Multiple Slide Images"

    @api.model
    def document_file_slide_upload(self, value, name, selected_ids, model):
        print('--------------------------',name)
        if selected_ids:
            data = value.split('base64')[1] if value else False
            for rec_id in selected_ids:
                slide_id = self.env['web.slide.image'].browse(rec_id)
                # AWS S3 credentials
                AWS_ACCESS_KEY = self.env['ir.config_parameter'].sudo().get_param(
                    'mis_website_backend.amazon_access_key')
                # AWS_ACCESS_KEY = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_access_key')
                AWS_SECRET_KEY = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_secret_key')
                BUCKET_NAME = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_bucket_name')
                REGION = self.env['ir.config_parameter'].get_param('mis_website_backend.amazon_region_name')
                if not AWS_ACCESS_KEY:
                    raise ValidationError(_("Please Add AWS Access Key"))
                if not AWS_SECRET_KEY:
                    raise ValidationError(_("Please Add AWS Secret Key"))
                if not BUCKET_NAME:
                    raise ValidationError(_("Please Add AWS Bucket Name"))
                if not REGION:
                    raise ValidationError(_("Please Add AWS Region Name"))
                session = boto3.session.Session(
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                    region_name=REGION,
                )
                s3 = session.resource('s3')

                file_name = name
                # file_content = base64.b64decode(datas[1])
                file_data = base64.b64decode(data)

                try:
                    s3.Bucket(BUCKET_NAME).put_object(
                        Key=file_name,
                        Body=file_data,
                        ContentType='image/jpg',
                        ACL='public-read'  # Or 'private'
                    )
                    s3_url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file_name}"
                    url_id = self.env['web.slide.image.url'].create({
                                                                        'slide_id' : slide_id.id,
                                                                        # 'sr_no' : sr_no,
                                                                        'url' : s3_url,
                                                                    })
                except Exception as e:
                    _logger.error(f"Error uploading to S3: {str(e)}")
            # self.env['ir.attachment'].create({
            #         'name': name,
            #         'datas': data,
            #         'res_model': model,
            #         'res_id': rec_id,
            #     })
            return True
