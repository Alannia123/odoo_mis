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
        all_announce_count = request.env['web.info'].sudo().search_count([('enable', '=', True)])
        today_announce_count = request.env['web.info'].sudo().search_count([('enable', '=', True),('date', '=', today_date)])
        partner = request.env.user.partner_id
        student_id = request.env['education.student'].sudo().search([('partner_id', '=', partner.id)])
        home_work_count = request.env['student.homework'].sudo().search_count([('class_div_id', '=', student_id.class_division_id.id)])
        today_home_work_count = request.env['student.homework'].sudo().search_count([('class_div_id', '=', student_id.class_division_id.id),
                                                                                                        ('homework_date', '=', today_date)])
        if request.env.user._is_internal():
            return request.render("portal.portal_my_home", values)
        else:
            return request.render("mis_student_portal.student_portal_my_home", {'all_announce_count' : all_announce_count,
                                                                            'today_announce_count' : today_announce_count,
                                                                            'student' : student_id,
                                                                            'div_name' : student_id.class_division_id.name,
                                                                            'home_work_count' : home_work_count,
                                                                            'attendance' : 'Present',
                                                                            'today_home_work_count' : today_home_work_count,
                                                                            })

    @route(['/school/student_info'], type='http', auth="user", website=True)
    def get_school_student_info(self, **kw):
        print('ghhgh33333333------==========')
        partner = request.env.user.partner_id
        student_id = request.env['education.student'].sudo().search([('partner_id', '=', partner.id)])
        return request.render("mis_student_portal.student_info", {'student': student_id})

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
        today_date = date.today()
        partner = request.env.user.partner_id
        student_id = request.env['education.student'].sudo().search([('partner_id', '=', partner.id)])
        print('ghhgh33333333------======all_homeworks====', student_id)
        home_work_ids = request.env['student.homework'].sudo().search([('class_div_id', '=', student_id.class_division_id.id)])
        today_home_work_ids = request.env['student.homework'].sudo().search([('class_div_id', '=', student_id.class_division_id.id),
                                                                             ('homework_date', '=', today_date)])
        print('ghhgh33333333------======all_homeworks====', home_work_ids)

        return request.render("mis_student_portal.portal_all_homeworks", {'homeworks': home_work_ids,
                                                                          'today_homework': today_home_work_ids})


    @route(['/homework/get_homework/<int:work_id>'],  type='http', auth="user", website=True)
    def get_school_get_homeworks(self, work_id=None, **kw):
        # homework_id = int(work_id)
        print('ghhgh33333333------======all_homeworks===homework_id=',work_id)
        home_work_id = request.env['student.homework'].sudo().browse(work_id)
        print('ghhgh33333333------======all_homeworks====', home_work_id)

        return request.render("mis_student_portal.portal_open_homeworks", {'home_work_id': home_work_id})


class CustomLogout(http.Controller):
    @http.route('/web/session/logout', type='http', auth="public", website=True)
    def logout(self, redirect='/web/login'):
        request.session.logout()
        return request.redirect(redirect)

