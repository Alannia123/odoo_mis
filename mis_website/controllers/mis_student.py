# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class StudentPortal(CustomerPortal):
    """Controller for creating a new portal design for student users"""

    @http.route(['/home'], type='http', auth="user", website=True)
    def student_portal(self):
        """New portal for student users"""
        return request.render("mis_website.student_portal")

    @http.route(['/student/info'], type='http', auth="user", website=True)
    def student_info(self):
        """Get basic details of students in the university"""
        values = request.env['university.student'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])
        full_name = values.name
        if values.middle_name:
            full_name = full_name + ' ' + values.middle_name
        if values.last_name:
            full_name = full_name + ' ' + values.last_name
        if values.gender == 'female':
            gender = 'Female'
        elif values.gender == 'male':
            gender = 'Male'
        else:
            gender = 'Other'
        vals = {
            'full_name': full_name,
            'student': values,
            'gender': gender,
        }
        return request.render("mis_website.student_info",
                              {'values': vals})

    @http.route(['/student/documents'], type='http', auth="user", website=True)
    def student_documents(self):
        """Get documents of students in the university"""
        student = request.env['university.student'].sudo().search([(
            'partner_id',
            '=',
            request.env.user.partner_id.id)]).application_id
        docs = request.env['university.document'].sudo().search(
            [('application_ref_id', '=', student.id)])
        attachment = request.env['ir.attachment'].sudo().browse(
            docs.attachment_ids.ids)
        attachment.public = True
        return request.render(
            "mis_website.student_documents",
            {'docs': docs})

    @http.route(['/student/exam/results'], type='http', auth="user",
                website=True)
    def student_exam_result(self):
        """Get exam results of students in the university"""
        student = request.env['university.student'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])
        exam = request.env['exam.result'].sudo().search(
            [('student_id', '=', student.id)])
        return request.render(
            "mis_website.student_exam_result",
            {'data': exam})

    @http.route(['/student/result'], type='http', auth="user",
                website=True)
    def exam_subject(self):
        """Get subject wise exam results of students in the university"""
        student = request.env['university.student'].sudo().search([(
            'partner_id',
            '=',
            request.env.user.partner_id.id)])
        exam = request.env['exam.result'].sudo().search(
            [('student_id', '=', student.id)])
        line = request.env['results.subject.line'].sudo().search(
            [('result_id', '=', exam.id)])
        data = {
            'exam': exam,
            'line': line
        }
        return request.render(
            "mis_website.student_result", data)

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        """ Overrided If the logged in user is a student,
                           they will be directed to the student portal."""
        values = self._prepare_portal_layout_values()
        if not request.env.user.partner_id.is_student:
            return request.render("portal.portal_my_home", values)
        else:
            return request.redirect('/home')
