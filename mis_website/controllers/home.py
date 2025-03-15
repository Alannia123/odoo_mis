# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo import fields, models, api, _


class home_controller(http.Controller):
    """Controller for taking Home"""

    @http.route('/mis_home', type='http', auth='public', website=True)
    def mis_home_temp(self):
        display_notice = ''
        print('SSSSSAAAAAAAAA',fields.Datetime.now())
        today_date = fields.Datetime.now().strftime('%d-%m-%Y')
        print('XXXXXXSSSSSSS',today_date)
        notices= request.env['web.info'].sudo().search([('enable', '=', True)])
        raw_html = ""
        for notice in notices:
            date = notice.date.strftime('%d-%m-%Y')
            raw_html = raw_html + f"""
                            <div style="text-align:center;">
                                <h4 style="color:blue;"><u>{date}</u></h2>
                                <p><strong>{notice.anounce}</strong>.</p>
                            </div><br/><br/>
                            """


        print('NOFGHDFHGD',display_notice)
        vals = {
            'today_date': today_date,
            'banner': request.env['banner.info'].sudo().search([('enable', '=', True)], limit=1),
            'notices': raw_html,
            # 'photos': request.env['program.gallery.photo'].sudo().search([]),
            # 'events': request.env['program.events'].sudo().search([]),
        }
        print('LODFFFFFFFFFFFFFFFFF',vals)
        return request.render('mis_website.mis_home_page', vals)
