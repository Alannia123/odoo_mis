# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationTimetableSchedule(models.Model):
    """Model representing the Timetable Schedule for specific periods."""
    _name = 'education.timetable.schedule'
    _description = 'Timetable Schedule'
    _rec_name = 'period_id'

    period_id = fields.Many2one('timetable.period', string="Period",
                                required=True, help="Select the period for the "
                                                    "timetable schedule.")
    time_from = fields.Float(string='From', required=True,
                             index=True, help="Start time of Period.")
    time_till = fields.Float(string='Till', required=True,
                             help="End time of Period.")
    subject_id = fields.Many2one('education.subject',
                                 string='Subjects',
                                 required=True,
                                 help="Subject associated with the schedule")
    faculty_id = fields.Many2one('education.faculty',
                                 string='Faculty',
                                 required=True, help="Faculty assigned with "
                                                     "the schedule")
    week_day = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Week', required=True,  help="Day of the week for the schedule.")
    timetable_id = fields.Many2one('education.timetable',
                                   string='Timetable',
                                   required=True, help="Timetable associated "
                                                       "with the schedule.")
    class_division_id = fields.Many2one('education.class.division',
                                        string='Class', readonly=True,
                                        help="Class division associated with"
                                             "the timetable schedule.")
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help="Company associated with timetable schedule")

    @api.model
    def create(self, vals):
        """Automatically stores division details fetched from timetable"""
        res = super().create(vals)
        res.class_division_id = res.timetable_id.class_division_id.id
        return res

    @api.onchange('period_id')
    def _onchange_period_id(self):
        """Gets the start and end time of the period"""
        self.time_from = self.period_id.time_from
        self.time_till = self.period_id.time_to

    @api.constrains('time_from', 'time_till', 'timetable_id')
    def _check_overlapping_schedules(self):
        """Method for avoiding time overlapping"""
        for record in self:
            if record.time_from >= record.time_till:
                raise ValidationError(
                    _("The start time must be before the end time."))
            overlapping_schedules = self.search([
                ('timetable_id', '=', record.timetable_id.id),
                ('id', '!=', record.id),
                ('week_day','=',record.week_day),
                '|', '&',
                ('time_from', '<', record.time_till),
                ('time_till', '>', record.time_from),
                '&',
                ('time_till', '>', record.time_from),
                ('time_from', '<', record.time_till)
            ])
            if overlapping_schedules:
                raise ValidationError(
                    _("The schedule times overlap with another schedule."))

