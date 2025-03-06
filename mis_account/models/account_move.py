# -*- coding: utf-8 -*-
from odoo import _, fields, api, Command, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError, AccessError


class AccountMove(models.Model):
    _inherit = 'account.move'



    signature = fields.Binary('Signature', copy=False, required=False)
