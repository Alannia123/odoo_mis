# -*- coding: utf-8 -*-

from odoo import fields, models
from firebase_admin import messaging, initialize_app, credentials, _apps
from odoo import models


class PushNotification(models.Model):
    """Using this class create the registration id for the user to send
        push notifications"""
    _name = 'push.notification'
    _description = 'Web Push Notification'

    user_id = fields.Many2one("res.users", string="Firebase User",
                              help="Corresponding Firebase User")
    register_id = fields.Char(string="Registration Id",
                              help="Firebase Registration Token")


    def _send_push_notification_mis(self, user, message, domain):
        """Send a push notification using Firebase."""
        print('MSDDDDDDDDDDDDDD',user)
        print('MSDDDDDDDDDDDDDD',message)
        print('MSDDDDDDDDDDDDDD',_apps)
        print('MSDDDDDDDDDDDDDD',domain)
        if not _apps:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": self.env.company.project_id_firebase,
                "private_key_id": self.env.company.private_key_ref,
                "private_key": self.env.company.private_key.replace('\\n',
                                                                    '\n'),
                "client_email": self.env.company.client_email,
                "client_id": self.env.company.client_id_firebase,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": self.env.company.client_cert_url,
                "universe_domain": "googleapis.com"
            })
            initialize_app(cred)
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title='Message from ' + user.name,
                body=message
            ),
            tokens=[reg_id.register_id for reg_id in
                    self.env['push.notification'].search(domain)]
        )
        messaging.send_each_for_multicast(message)
