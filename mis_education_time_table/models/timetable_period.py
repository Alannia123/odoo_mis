# -*- coding: utf-8 -*-

from odoo import models, fields


class TimetablePeriod(models.Model):
    """Model representing the Periods in the Timetable."""
    _name = 'timetable.period'
    _description = 'Timetable Period'

    name = fields.Char(string="Name", required=True, help="Name of the "
                                                          "timetable period")
    time_from = fields.Float(string='From', required=True,
                             index=True, help="Start time of Period.")
    time_to = fields.Float(string='To', required=True, help="End time of "
                                                            "Period")
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help="Company associated with timetable schedule")
