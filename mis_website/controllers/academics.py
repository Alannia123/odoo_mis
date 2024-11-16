# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request


class mis_academics(http.Controller):
    """Controller for taking Prospectus"""

    @http.route('/mis_academics', type='http', auth='public', website=True)
    def academic_mis_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.mis_academics')

    @http.route('/student_performance', type='http', auth='public', website=True)
    def mis_student_performance_cont(self):
        """To redirect to contact page."""
        return request.render('mis_website.student_performance')

