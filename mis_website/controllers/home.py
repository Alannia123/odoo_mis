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
        today_date = fields.Datetime.now().strftime('%d-%m-%Y')
        notices= request.env['web.info'].sudo().search([('enable', '=', True)])
        raw_html = ""
        for notice in notices:
            date = notice.date.strftime('%d-%m-%Y')
            raw_html = raw_html + f"""
                            <div style="text-align:center;">
                                <h4 style="color:#331a00;"><u>{date}</u></h2>
                                <span style="color: {notice.color};"><strong >{notice.anounce}</strong>.</span>
                            </div><br/>
                            """
        today = datetime.today().strftime('%m-%d')  # Get today's MM-DD format
        query = """
                    SELECT id
                    FROM education_student
                    WHERE TO_CHAR(date_of_birth, 'MM-DD') = %s
                """
        # request.env.cr.execute(query, (today,))
        # stu_birth_ids = request.env.cr.fetchall()
        # print('DDDDWWWWWWWWWWWWWW',stu_birth_ids)
        students = request.env['education.student'].sudo().search([])
        birthday_students = students.filtered(lambda s: s.date_of_birth.strftime('%m-%d') == today)
        birth_raw_html = ""
        sr_no = 1
        for student_id in birthday_students:
            print('dddddddddgggggggggggggggg',student_id)
            # student_id = request.env['education.student'].browse(stu_id)
            if student_id:
                birth_raw_html = birth_raw_html + f"""
                                <div style="text-align:left;">
                                    <span style="color: #992600;">{sr_no})<strong >{student_id.name}({student_id.class_division_id.name})</strong>.</span>
                                </div>
                                """
                sr_no = sr_no + 1
        print('eeeeeeeeee',birth_raw_html)
        birth_raw_html = birth_raw_html + f"""<br/><h1 class="birthday-wish text-center">Happy Birthday! 🎉</h1>"""
        vals = {
            'today_date': today_date,
            'banner': request.env['banner.info'].sudo().search([('enable', '=', True)], limit=1),
            'notices': raw_html,
            'birth_raw_html': birth_raw_html,
            'today_births': birthday_students,
            # 'photos': request.env['program.gallery.photo'].sudo().search([]),
            # 'events': request.env['program.events'].sudo().search([]),
        }
        return request.render('mis_website.mis_home_page', vals)
