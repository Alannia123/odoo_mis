import calendar
from datetime import date

from odoo import http, tools, _, SUPERUSER_ID
from odoo.exceptions import AccessDenied, AccessError, MissingError, UserError, ValidationError
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import consteq
from datetime import date



class WebsiteAttendance(http.Controller):

    @http.route('/school/student_attendance', type='http', auth='user', website=True)
    def view_attendance(self, month=None, year=None):
        partner = request.env.user.partner_id
        student_id = request.env['education.student'].sudo().search([('partner_id', '=', partner.id)])
        today = date.today()
        year = int(year) if year else today.year
        month = int(month) if month else today.month

        # Get weekday of first day and total days in month
        first_weekday, total_days = calendar.monthrange(year, month)

        calendar.setfirstweekday(calendar.SUNDAY)
        month_matrix = calendar.monthcalendar(year, month)

        # Get attendance records
        records = request.env['education.attendance.line'].sudo().search([
            # ('attendance_id', '!=', False),
            ('state', '=', 'done'),
            ('student_id', '=', student_id.id),
            ('date', '>=', date(year, month, 1)),
            ('date', '<=', date(year, month, total_days))
        ])


        # Map attendance status by day
        status_by_day = {}
        for rec in records:
            if rec.present_morning:
                status_by_day.update({rec.date.day: 'present'})
            else:
                status_by_day.update({rec.date.day: 'absent'})

        # For prev/next buttons
        prev_month = month - 1 or 12
        prev_year = year - 1 if prev_month == 12 else year
        next_month = month + 1 if month < 12 else 1
        next_year = year + 1 if next_month == 1 else year

        # status_by_day = {r.date.day: r.status for r in records}

        # Prepare weeks (each week = 7 days, with None where no day exists)

        return request.render('mis_student_portal.template_attendance_calendar', {
            'month': calendar.month_name[month],
            'month_num': month,
            'year': year,
            'weeks': month_matrix,
            'status_by_day': status_by_day,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
        })
