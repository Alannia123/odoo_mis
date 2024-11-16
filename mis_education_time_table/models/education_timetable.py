# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


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
