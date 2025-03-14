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
        print('ghhgh33333333------==========')
        announce_count = request.env['web.info'].sudo().search_count([('enable', '=', True)])
        # values = self._prepare_portal_layout_values()
        print('ghhgh33333333------==========',announce_count)
        return request.render("mis_student_portal.student_portal_my_home", {'announce_count' : announce_count})

    @route(['/school/announcements'], type='http', auth="user", website=True)
    def get_school_announcements(self, **kw):
        print('ghhgh33333333------==========')
        announce_count = request.env['web.info'].sudo().search([('enable', '=', True)])
        # values = self._prepare_portal_layout_values()
        print('ghhgh33333333------==========', announce_count)
        return request.render("mis_student_portal.student_school_announcements", {'announce_count': announce_count})
