# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Gokul PI (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def has_push_notification_permission(self):
        return self.has_group('base.group_user')


#
# from odoo import models, fields
# import requests
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     firebase_browser_token = fields.Char("Firebase Browser Token")
#
#     def send_firebase_notification(self, title, message):
#         self.ensure_one()
#         server_key = "YOUR_FIREBASE_SERVER_KEY"
#         headers = {
#             "Authorization": f"key={server_key}",
#             "Content-Type": "application/json"
#         }
#
#         payloads = []
#
#         if self.firebase_browser_token:
#             payloads.append({
#                 "to": self.firebase_browser_token,
#                 "notification": {
#                     "title": title,
#                     "body": message,
#                     "icon": "https://yourwebsite.com/icon.png"
#                 }
#             })
#
#         if self.firebase_mobile_token:
#             payloads.append({
#                 "to": self.firebase_mobile_token,
#                 "notification": {
#                     "title": title,
#                     "body": message,
#                     "icon": "https://yourwebsite.com/icon.png",
#                     "click_action": "FLUTTER_NOTIFICATION_CLICK"
#                 },
#                 "priority": "high"
#             })
#
#         for payload in payloads:
#             requests.post("https://fcm.googleapis.com/fcm/send", json=payload, headers=headers)
#
# #
# class taskmag(models.Model):
#     _inherit = 'task.management'
#
#     def action_assign_to_faculty(self):
#         res = super(taskmag, self).action_assign_to_faculty()
#         for order in self:
#             order.user_id.send_firebase_notification(
#                 "New Sale Order Confirmed",
#                 f"Order {order.name} has been confirmed."
#             )
#         return res
#
#
