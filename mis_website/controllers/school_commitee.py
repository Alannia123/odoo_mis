# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request


class mis_academic_exam_commitee(http.Controller):
    """Controller for taking Prospectus"""

    @http.route('/academic_exam_commitee', type='http', auth='public', website=True)
    def academic_exam_commitee_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.academic_exam_commitee')

    @http.route('/english_lit_club', type='http', auth='public', website=True)
    def english_lit_club_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.english_lit_club')

    @http.route('/bengali_lit_club', type='http', auth='public', website=True)
    def bengali_lit_club_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.bengali_lit_club')

    @http.route('/eco_club', type='http', auth='public', website=True)
    def eco_club_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.eco_club')


    @http.route('/cultural_club', type='http', auth='public', website=True)
    def cultural_club_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.cultural_club')


    @http.route('/sports_club', type='http', auth='public', website=True)
    def sports_club_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.sports_club')


    @http.route('/students_council', type='http', auth='public', website=True)
    def students_council_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.students_council')


    @http.route('/staff_menbers', type='http', auth='public', website=True)
    def staff_menbers_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.staff_menbers')

