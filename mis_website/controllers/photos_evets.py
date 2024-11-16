# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request


class program_events_controller(http.Controller):
    """Controller for taking Prospectus"""

    @http.route('/program_events_gallery', type='http', auth='public', website=True)
    def program_events_gallery_cont(self):
        """To redirect to contact page."""

        vals = {
            'photos': request.env['ir.attachment'].sudo().search([('res_model', '=', 'program.gallery')]),
            'events': request.env['program.events'].sudo().search([]),
        }
        print('LODFFFFFFFFFFFFFFFFF',vals)
        return request.render('mis_website.program_events_gallery', vals)


    @http.route(['/gallery/photos/<int:event>'], type='http', auth="public", website=True)
    def get_event_galarry(self, event=None, **kw):
        photo_gallery = request.env['program.gallery'].sudo().search([('id', '=', int(event))])
        print('DDDDDDDEEEEEEWWWWWWWWWWW',photo_gallery)
        values = {
                    'gallery': photo_gallery,
                }
        return request.render("mis_website.program_events_gallery_individual_event", values)

