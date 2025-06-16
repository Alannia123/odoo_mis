# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    firebase_token = fields.Char("Firebase Token")

    def has_push_notification_permission(self):
        return self.has_group('base.group_user')
