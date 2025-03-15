# -*- coding: utf-8 -*-
import base64
import json
import math
import re

from werkzeug import urls

from odoo import http, tools, _, SUPERUSER_ID
from odoo.exceptions import AccessDenied, AccessError, MissingError, UserError, ValidationError
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import consteq
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalCustom(CustomerPortal):
    """Controller for taking Home"""


    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        announce_count = request.env['web.info'].sudo().search_count([('enable', '=', True)])
        print('ghhgh33333333------==========', announce_count)
        # if not request.env.user.partner_id.is_student:
        #     return request.render("portal.portal_my_home", values)
        # else:
        return request.render("mis_student_portal.student_portal_my_home", {'announce_count' : announce_count})

    @route(['/school/announcements'], type='http', auth="user", website=True)
    def get_school_announcements(self, **kw):
        print('ghhgh33333333------==========')
        display_notice = ''
        notices = request.env['web.info'].sudo().search([('enable', '=', True)])
        raw_html = ""
        for notice in notices:
            date = notice.date.strftime('%d-%m-%Y')
            raw_html = raw_html + f"""
                                    <div style="text-align:center;">
                                        <h4 style="color:blue;"><u>{date}</u></h2>
                                        <p><strong>{notice.anounce}</strong>.</p>
                                    </div><br/><br/>
                                    """
        # values = self._prepare_portal_layout_values()
        return request.render("mis_student_portal.student_school_announcements", {'notices': raw_html})
