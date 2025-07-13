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
        vals = {}
        display_notice = ''
        today_date = fields.Datetime.now().strftime('%d-%m-%Y')
        # slide_id = request.env['web.slide.image'].sudo().search([('enable', '=', True)])
        # if slide_id.image_url_ids[0]:
        #     vals.update({'slide_1': slide_id.image_url_ids[0].url })
        # if slide_id.image_url_ids[1]:
        #     vals.update({'slide_2': slide_id.image_url_ids[1].url })
        # # if slide_id.image_url_ids[2]:
        #     vals.update({'slide_3': slide_id.image_url_ids[2].url })
        # if slide_id.image_url_ids[3]:
        #     vals.update({'slide_4': slide_id.image_url_ids[3].url })
        # if slide_id.image_url_ids[4]:
        #     vals.update({'slide_5': slide_id.image_url_ids[4].url })
        # if slide_id.image_url_ids[5]:
        #     vals.update({'slide_6': slide_id.image_url_ids[5].url })
        # if slide_id.image_url_ids[6]:
        #     vals.update({'slide_7': slide_id.image_url_ids[6].url })

        video_id= request.env['web.video'].sudo().search([('show_website', '=', True)], limit=1)
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
        member_id = request.env['school.members'].sudo().search([])
        students = request.env['education.student'].sudo().search([])
        birthday_students = students.filtered(lambda s: s.date_of_birth.strftime('%m-%d') == today)
        birth_raw_html = ""
        sr_no = 1
        for student_id in birthday_students:
            # student_id = request.env['education.student'].browse(stu_id)
            if student_id:
                birth_raw_html = birth_raw_html + f"""
                                <div style="text-align:left;">
                                    <span style="color: #992600;">{sr_no})<strong >{student_id.name}({student_id.class_division_id.name})</strong>.</span>
                                </div>
                                """
                sr_no = sr_no + 1
        birth_raw_html = birth_raw_html + f"""<br/><h1 class="birthday-wish text-center">Happy Birthday! 🎉</h1>"""
        vals = {
            'today_date': today_date,
            'banner': request.env['banner.info'].sudo().search([('enable', '=', True)], limit=1),
            'notices': raw_html,
            'birth_raw_html': birth_raw_html,
            'today_births': birthday_students,
            'member_id': member_id,
            'video_id': video_id,
            # 'slide_id': slide_id,
            'birth_background': 'mis_website/',
            }
        print('UTTTTTTTTTTTTTTTTT',vals)
        return request.render('mis_website.mis_home_page', vals)

    @http.route('/privacy_policy', type='http', auth='public', website=True)
    def mis_school_privacy_policy(self):
        """To redirect to contact page."""
        magazines = request.env['school.magazine'].sudo().search([('state', '=', 'post')])
        return request.render('mis_website.mis_school_privacy_policy')
