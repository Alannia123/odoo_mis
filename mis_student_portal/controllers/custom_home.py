from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home

class CustomHome(Home):
    @http.route('/web', type='http', auth="user", website=True)
    def web_client(self, s_action=None, **kw):
        return http.local_redirect('/web#menu_id=42')  # Replace 'apps_menu_id' with actual menu ID
