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
        for notice in notices:
            date = notice.date.strftime('%d-%m-%Y')
            display_notice = display_notice + str(date) + ' - ' + str(notice.anounce) + '\n\n'


        print('NOFGHDFHGD',display_notice)
        vals = {
            'today_date': today_date,
            'banner': request.env['banner.info'].sudo().search([('enable', '=', True)], limit=1),
            'notices': display_notice,
            # 'photos': request.env['program.gallery.photo'].sudo().search([]),
            # 'events': request.env['program.events'].sudo().search([]),
        }
        print('LODFFFFFFFFFFFFFFFFF',vals)
        return request.render('mis_website.mis_home_page', vals)
