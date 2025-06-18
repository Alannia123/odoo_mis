# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request
import json


class program_events_controller(http.Controller):
    """Controller for taking Prospectus"""

    @http.route('/program_events_gallery', type='http', auth='public', website=True)
    def program_events_gallery_cont(self):
        """To redirect to contact page."""

        vals = {
            'events': request.env['program.gallery.aws'].sudo().search([]),
        }
        print('LODFFFFFFFFFFFFFFFFF',vals)
        return request.render('mis_website.program_events_gallery', vals)


    @http.route(['/gallery/photos/<int:event>'], type='http', auth="public", website=True)
    def get_event_galarry(self, event=None, **kw):
        photo_gallery = request.env['program.gallery.aws'].sudo().search([('id', '=', int(event))])
        print('DDDDDDDEEEEEEWWWWWWWWWWW',photo_gallery)
        values = {
                    'gallery': photo_gallery,
                }
        return request.render("mis_website.program_events_gallery_individual_event", values)

    @http.route('/calendar/events', type='json', auth="public")
    def get_calendar_events(self, **kwargs):
        events = request.env['calendar.event'].sudo().search([])
        print('tfghhgfhgfhg',events)
        data = [{
            'title': event.name,
            'start': event.start,
            'end': event.stop,
        } for event in events]
        return json.dumps(data)

