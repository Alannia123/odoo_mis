from odoo import models, fields, api , _
from odoo.exceptions import UserError
import re

class AdvanceLoginForm(models.Model):
    _inherit = 'res.users'
    @api.model

    def signup(self, values, token=None):
        password = values.get('password')
        if password and not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[a-zA-Z\d@$!%*?&]{8,}$', password):
            error_message = _("Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")
            raise UserError(error_message)
        else:
            return super(AdvanceLoginForm, self).signup(values, token)
    

