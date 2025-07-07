# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import requests
import base64
import logging

_logger = logging.getLogger(__name__)


class EducationTimetable(models.Model):
    """Model representing the Timetable for classes."""
    _name = 'education.timetable'
    _description = 'Timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string='Active', default=True,
                            help="Set to False to deactivate the timetable.")
    name = fields.Char(string='Name',
                       help="Generated name based on class, division, "
                            "and academic year.")
    class_division_id = fields.Many2one('education.class.division',
                                        string='Class', required=True,
                                        help="Select the class and division for"
                                             "the timetable."
                                        )
    class_name_id = fields.Many2one('education.class',
                                    string="Standard",
                                    related='class_division_id.class_id',
                                    help="Standard associated with the "
                                         "timetable.")
    division_name_id = fields.Many2one('education.division',
                                       string='Division', help="Division of "
                                                               "the class",
                                       related='class_division_id.division_id')
    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Academic Year', readonly=True,
                                       related='class_division_id.academic_year_id',
                                       help="Academic year of the class")
    timetable_mon_ids = fields.One2many('education.timetable.schedule',
                                        'timetable_id',
                                        string='Monday Timetable',
                                        domain=[('week_day', '=', '0')],
                                        help="Timetable schedules for Monday.")
    timetable_tue_ids = fields.One2many('education.timetable.schedule',
                                        'timetable_id',
                                        string='Tuesday Timetable',
                                        domain=[('week_day', '=', '1')],
                                        help="Timetable schedules for Tuesday.")
    timetable_wed_ids = fields.One2many('education.timetable.schedule',
                                        'timetable_id',
                                        string='Wednesday Timetable',
                                        domain=[('week_day', '=', '2')],
                                        help="Timetable schedules for "
                                             "Wednesday.")
    timetable_thur_ids = fields.One2many('education.timetable.schedule',
                                         'timetable_id',
                                         string='Thursday Timetable',
                                         domain=[('week_day', '=', '3')],
                                         help="Timetable schedules for "
                                              "Thursday.")
    timetable_fri_ids = fields.One2many('education.timetable.schedule',
                                        'timetable_id',
                                        string='Friday Timetable',
                                        domain=[('week_day', '=', '4')],
                                        help="Timetable schedules for Friday.")
    timetable_sat_ids = fields.One2many('education.timetable.schedule',
                                        'timetable_id',
                                        string='Saturday Timetable',
                                        domain=[('week_day', '=', '5')],
                                        help="Timetable schedules for "
                                             "Saturday.")
    timetable_sun_ids = fields.One2many('education.timetable.schedule',
                                        'timetable_id',
                                        string='Sunday Timetable',
                                        domain=[('week_day', '=', '6')],
                                        help="Timetable schedules for Sunday.")
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help="Company associated with the timetable.")
    pdf_file = fields.Binary(string="Upload TimeTable", attachment=True)
    file_name = fields.Char('File Name')
    preview_image = fields.Binary(string="PDF Preview", readonly=True)
    facebook_photo_url = fields.Char("Facebook Photo URL")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], 'State', default='draft', tracking=True)

    def set_to_post(self):
        if self.pdf_file:
            self.state = 'done'

    def reste_to_draft(self):
        self.state = 'draft'



    def upload_photo_to_facebook(self, image_data, caption=""):
        page_access_token = 'YOUR_PAGE_ACCESS_TOKEN'
        page_id = 'YOUR_PAGE_ID'

        # Convert binary image to a temporary file or base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # Facebook Graph API endpoint
        url = f"https://graph.facebook.com/{page_id}/photos"

        payload = {
            'caption': caption,
            'access_token': page_access_token,
            'published': 'true',
        }

        files = {
            'source': image_data,
        }

        response = requests.post(url, data=payload, files=files)

        if response.status_code == 200:
            res_json = response.json()
            post_id = res_json.get('post_id')
            photo_id = res_json.get('id')
            photo_url = f"https://www.facebook.com/{photo_id}"
            return photo_url
        else:
            _logger.error("Facebook upload failed: %s", response.text)
            return None

    @api.onchange('pdf_file')
    def _generate_preview(self):
        if self.pdf_file:
            self.preview_image = self.pdf_file
        else:
            self.preview_image = False


    def create(self, vals_list):
        if ('class_division_id' in vals_list.keys() and
                vals_list['class_division_id']):
            class_division = self.env['education.class.division'].browse(
                vals_list['class_division_id'])
            vals_list['name'] = "/".join([class_division.class_id.name,
                                          class_division.name,
                                          class_division.academic_year_id.name])
        return super().create(vals_list)

    @api.constrains('class_division_id')
    def _check_class_division_id(self):
        """Check duplication of record"""
        for record in self:
            duplicate_records = self.search([
                ('class_division_id', '=', record.class_division_id.id),
                ('academic_year_id', '=', record.academic_year_id.id),
                ('id', '!=', record.id)  # Exclude current record
            ])
            if duplicate_records:
                raise ValidationError(
                    'Timetable for %s already exist' % (
                        record.class_division_id.name))
