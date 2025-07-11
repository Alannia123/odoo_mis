# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationAttendanceLine(models.Model):
    """Used for managing attendance shift details"""
    _name = 'education.attendance.line'
    _description = 'Attendance Lines'

    name = fields.Char(string='Name', help="Name of Attendance")
    attendance_id = fields.Many2one('education.attendance',
                                    string='Attendance Id', ondelete='cascade',
                                    help="Connected Attendance")
    student_id = fields.Many2one('education.student',
                                 string='Student',
                                 help="Student ID for the attendance")
    register_no = fields.Char(related='student_id.register_no', string='Registration Number', required=True, readonly=True)
    roll_no = fields.Char(related='student_id.roll_no', string='Roll Number', readonly=True)
    student_name = fields.Char(string='Student', related='student_id.name',
                               help="Student name for attendance")
    class_id = fields.Many2one('education.class', string='Class',
                               required=True,
                               help="Enter class for attendance")
    division_id = fields.Many2one('education.class.division',
                                  string='Division',
                                  help="Enter class division for attendance",
                                  required=True)
    date = fields.Date(string='Date', required=True, help="Date of attendance")
    present_morning = fields.Boolean(string='Present/Absent',
                                     help="Enable if the student is present "
                                          "in the morning.")
    # present_afternoon = fields.Boolean(string='After Noon',
    #                                    help="Enable if the student is present "
    #                                         "in the afternoon")
    full_day_absent = fields.Integer(string='Full Day',
                                     help="Full day present or not")
    # half_day_absent = fields.Integer(string='Half Day',
    #                                  help="Half present or not")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             string='State', default='draft',
                             help="Stages of student every day attendance")
    company_id = fields.Many2one(
        'res.company', string='Company', help="Current Company",
        default=lambda self: self.env.company)
    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Academic Year',
                                       related='division_id.academic_year_id',
                                       help="Academic year of education")
