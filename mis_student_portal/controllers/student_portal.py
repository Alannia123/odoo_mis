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
from datetime import date


class CustomerPortalCustom(CustomerPortal):
    """Controller for taking Home"""


    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        today_date = date.today()
        all_count = request.env['web.info'].sudo().search_count([('enable', '=', True)])
        today_count = request.env['web.info'].sudo().search_count([('enable', '=', True),('date', '=', today_date)])
        # if not request.env.user.partner_id.is_student:
        #     return request.render("portal.portal_my_home", values)
        # else:
        return request.render("mis_student_portal.student_portal_my_home", {'all_count' : all_count,
                                                                            'today_count' : today_count})

    @route(['/school/announcements'], type='http', auth="user", website=True)
    def get_school_announcements(self, **kw):
        print('ghhgh33333333------==========')
        display_notice = ''
        notices = request.env['web.info'].sudo().search([('enable', '=', True)])
        raw_html = ""
        for notice in notices:
            date = notice.date.strftime('%d-%m-%Y')
            raw_html = raw_html + f""" <div style="text-align:center;">
                                <h4 style="color:#331a00;"><u>{date}</u></h2>
                                <span style="color: {notice.color};"><strong >{notice.anounce}</strong>.</span>
                            </div><br/><br/>
                            """
        # values = self._prepare_portal_layout_values()
        return request.render("mis_student_portal.student_school_announcements", {'notices': raw_html})


    @route(['/school/all_homeworks'], type='http', auth="user", website=True)
    def get_school_all_homeworks(self, **kw):
        print('ghhgh33333333------======all_homeworks====',request.env.user.partner_id)
        partner = request.env.user.partner_id
        student_id = request.env['education.student'].sudo().search([('partner_id', '=', partner.id)])
        print('ghhgh33333333------======all_homeworks====', student_id)
        home_work_ids = request.env['student.homework'].sudo().search([('class_div_id', '=', student_id.class_division_id.id)])
        print('ghhgh33333333------======all_homeworks====', home_work_ids)

        return request.render("mis_student_portal.portal_all_homeworks", {'homeworks': home_work_ids})


    @route(['/homework/get_homework/<int:work_id>'],  type='http', auth="user", website=True)
    def get_school_get_homeworks(self, work_id=None, **kw):
        # homework_id = int(work_id)
        print('ghhgh33333333------======all_homeworks===homework_id=',work_id)
        partner = request.env.user.partner_id
        student_id = request.env['education.student'].sudo().search([('partner_id', '=', partner.id)])
        print('ghhgh33333333------======all_homeworks====', student_id)
        home_work_ids = request.env['student.homework'].sudo().search([('class_div_id', '=', student_id.class_division_id.id)])
        print('ghhgh33333333------======all_homeworks====', home_work_ids)

        return request.render("mis_student_portal.portal_all_homeworks", {'homeworks': home_work_ids})


class CustomLogout(http.Controller):
    @http.route('/web/session/logout', type='http', auth="public", website=True)
    def logout(self, redirect='/web/login'):
        request.session.logout()
        return request.redirect(redirect)
