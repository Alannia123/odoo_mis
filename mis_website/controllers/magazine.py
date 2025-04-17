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
    def mis_school_e_magazine(self):
        """To redirect to contact page."""
        magazines = request.env['school.magazine'].sudo().search([('state', '=', 'post')])
        return request.render('mis_website.template_magazine_list', {'magazines': magazines})

    @http.route('/e-magazine/view/<int:magazine_id>', type='http', auth='public', website=True)
    def view_magazine(self, magazine_id, **kwargs):
        magazine = request.env['school.magazine'].sudo().browse(magazine_id)
        pdf_data_uri = f"/web/content/{magazine.attachment_id.id}?download=false"
        raw_html_content = f"""<iframe src="{pdf_data_uri}" width="100%" height="600px"></iframe>"""
        # pdf_url = f"/web/content/{magazine.id}/pdf_file/{magazine.file_name}"
        # pdf_url = f"http://localhost:8069/web/content/{magazine.id}?field=pdf_file&filename={magazine.file_name}"
        return request.render('mis_website.template_magazine_view', {'magazine': magazine,
                                                                     'raw_html_content' : raw_html_content,
                                                                     })