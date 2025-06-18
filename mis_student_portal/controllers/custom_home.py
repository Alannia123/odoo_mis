from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
#
# class CustomLoginRedirect(Website):
#
#
#     def _login_redirect(self, uid, redirect=None):
#         """ Redirect regular users (employees) to the backend) and others to
#         the frontend
#         """
#         print('CCCCCCCCFFFFFFFFFFFFFFFFF============',redirect)
#         if not redirect and request.params.get('login_success'):
#             if request.env['res.users'].browse(uid)._is_internal():
#                 redirect = '/web#action=747&cids=1&menu_id=543'
#             else:
#                 redirect = '/my'
#         return super()._login_redirect(uid, redirect=redirect)

# controllers/main.py

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home

class CustomAuth(Home):

    @http.route('/web/login', type='http', auth="none", csrf=False, website=True)
    def web_login(self, redirect=None, **kw):
        response = super().web_login(redirect=redirect, **kw)
        # If login successful (uid is set), redirect to custom action
        if request.httprequest.method == 'POST' and request.session.uid:
            # Redirect to your action
            return http.redirect_with_hash('/web#action=education_erp_dashboard_action')

        return response





class CustomLogout(http.Controller):
    @http.route('/web/session/logout', type='http', auth="public", website=True)
    def logout(self, redirect='/web/login'):
        request.session.logout()
        return request.redirect(redirect)


