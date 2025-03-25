# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo import _
from odoo.http import request, route, Controller, content_disposition
import io



class Emagazine(http.Controller):
    """Controller for taking online admission"""

    @http.route('/e_magazine', type='http', auth='public', website=True)
    def school_e_magazine(self):
        """To redirect to contact page."""
        magazines = request.env['school.magazine'].sudo().search([('state', '=', 'post')])
        return request.render('mis_website.template_magazine_list', {'magazines': magazines})

    @http.route('/e-magazine/view/<int:magazine_id>', type='http', auth='public', website=True)
    def view_magazine(self, magazine_id, **kwargs):
        magazine = request.env['school.magazine'].sudo().browse(magazine_id)
        if not magazine or not magazine.pdf_file:
            return request.not_found()
        pdf_base64 = base64.b64encode(magazine.pdf_file).decode('utf-8')
        pdf_data_uri = f"data:application/pdf;base64,{pdf_base64}"
        pdf_url = f"/web/content/{magazine.id}/pdf_file/{magazine.file_name}"
        pdf_url = f"http://localhost:8069/web/content/{magazine.id}?field=pdf_file&filename={magazine.file_name}"
        # print('dddddddddddddd',pdf_data_uri)
        return request.render('mis_website.template_magazine_view', {'magazine': magazine,
                                                                     'pdf_data_uri' : pdf_data_uri,
                                                                     'pdf_url' : pdf_url
                                                                     })