from odoo import http
from odoo.http import request
import calendar
from datetime import date

class WebsiteSchoolEvent(http.Controller):

    @http.route(['/school/calendar'], type='http', auth='public', website=True)
    def wall_calendar(self, **kwargs):
        today = date.today()
        year = int(kwargs.get('year') or today.year)
        month = int(kwargs.get('month') or today.month)

        _, num_days = calendar.monthrange(year, month)
        first_day = date(year, month, 1)
        first_weekday = first_day.weekday()
        start_offset = (first_weekday + 1) % 7

        events_by_date = {
            e.event_date: e for e in request.env['school.event'].sudo().search([
                ('is_published', '=', True),
                ('event_date', '>=', f'{year}-{month:02d}-01'),
                ('event_date', '<=', f'{year}-{month:02d}-{num_days}')
            ])
        }

        calendar_cells = []
        total_cells = start_offset + num_days
        for i in range(total_cells):
            if i < start_offset:
                calendar_cells.append({'day': '', 'event': None})
            else:
                day = i - start_offset + 1
                ed = date(year, month, day)
                calendar_cells.append({
                    'day': day,
                    'event': events_by_date.get(ed)
                })

        month_name = date(year, month, 1).strftime('%B')

        return request.render('mis_website.template_school_event_wall_calendar', {
            'calendar_data': calendar_cells,
            'month_name': month_name,
            'year': year,
            'month': month,  # for navigation
        })