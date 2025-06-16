# -*- coding: utf-8 -*-

from firebase_admin import messaging, initialize_app, credentials, _apps
from odoo import models
import logging
_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    """Inherits MailThread to send notifications using chatterbox"""
    _inherit = 'mail.thread'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """Override the _notify_thread() function to fetch chat message details
        and push that message as a notification."""
        res = super()._notify_thread(message, msg_vals=msg_vals, **kwargs)
        msg = message.read()
        if (self.env.company.push_notification and self.env.user.has_group('base.group_user')):
            try:
                domain = []
                receiver_ids = self._get_receiver_ids(msg)
                user_list = [rec.id for rec in receiver_ids]

                if receiver_ids:
                    domain = [('user_id', 'in', user_list)]
                self._send_push_notification(msg, domain)
            except Exception as e:
                self.env['ir.logging'].sudo().create({
                    'name': 'Push Notification Error',
                    'type': 'server',
                    'level': 'ERROR',
                    'message': str(e),
                    'path': 'mail.thread',
                    'func': '_notify_thread',
                    'line': '45',
                })
        return res

    def _get_receiver_ids(self, msg):
        """Identify the receiver(s) of the notification for threaded and channel models."""
        receiver_ids = []

        if self._name == 'mail.channel':
            # Handle Discuss channel
            for partner in self.channel_partner_ids:
                if partner.id != msg[0]['author_id'][0]:
                    user = self.env['res.users'].search([('partner_id', '=', partner.id)], limit=1)
                    if user:
                        receiver_ids.append(user)
        else:
            # Handle threaded custom models
            if msg[0].get('author_id'):
                author_partner_id = msg[0]['author_id'][0]
                follower_partners = self.message_follower_ids.mapped('partner_id')
                for partner in follower_partners:
                    if partner.id != author_partner_id:
                        user = self.env['res.users'].search([('partner_id', '=', partner.id)], limit=1)
                        if user:
                            receiver_ids.append(user)

        return receiver_ids

    # def _get_receiver_ids(self, msg):
    #     """Identify the receiver of the notification."""
    #     receiver_ids = []
    #     receiver_id = False
    #     if self.channel_type != 'channel':
    #         for partner in self.channel_partner_ids:
    #             if partner.id != msg[0]['author_id'][0]:
    #                 receiver_id = self.env['res.users'].search([('partner_id', '=', partner.id)])
    #             if receiver_id:
    #                 receiver_ids.append(receiver_id)
    #     else:
    #         for partner in self.channel_partner_ids:
    #             receiver_id = self.env['res.users'].search([('partner_id', '=', partner.id)])
    #             if receiver_id:
    #                 receiver_ids.append(receiver_id)
    #     return receiver_ids



    def _send_push_notification(self, msg, domain):
        """Send a push notification using Firebase."""
        print('DOMAI-------------------',domain)
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
            notification=messaging.Notification( title='Message from ' + msg[0]['author_id'][1], body=msg[0]['body']),
                                                            tokens=[reg_id.register_id for reg_id in  self.env['push.notification'].search(domain)])
        messaging.send_each_for_multicast(message)

    def message_post(self, **kwargs):
        res = super().message_post(**kwargs)

        # Find users to notify (e.g., followers)
        followers = self.message_follower_ids.mapped('partner_id.user_ids')
        print('DDDDDDDDRRRRRRRRRRRRRRR',followers)
        # ffdfdg
        for user in followers:
            self.send_firebase_notification(user, kwargs.get('body'))

        return res

    def send_firebase_notification(self, user, message):
        # Send push to the user's Firebase token
        firebase_token = False
        print('rrrrrrrrrrrrrrrrrrrr',user)
        print('rrrrrrrrrrrrrrrrrrrr',user.firebase_token)
        token_id = self.env['push.notification'].search([('user_id', '=', user.id)], limit=1)
        if token_id:
            firebase_token = token_id.register_id
        print('rrrrrrrrrrrrrrrrrrrrqqqqqqqqqq', token_id)
        print('rrrrrrrrrrrrrrrrrrrrqqqqqqqqqq', firebase_token)
        # firebase_token = 'cZ-OSVYW-NF1e27DyBz9pA:APA91bGfw1L2T_x25gAiQXvbbaqUuecTfmGUWnBPNwYWfWJzWgRa9OF3jr8sAMyl4OopvjLLbMhwpI5Yeop2qJJq2ikxYeAKYnPzMg9K0j7XrP5oRf7KT4w'
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
        try:
            messaging.send(messaging.Message(
                notification=messaging.Notification(
                    title="New Message in Odoo",
                    body=message or "You have a new message",
                ),
                token=user.firebase_token,
                webpush=messaging.WebpushConfig(
                    notification=messaging.WebpushNotification(
                        icon="/mail_push_notification/static/src/img/schoollogo.ico",
                    )
                )
            ))
        except Exception as e:
            _logger.warning(f"Failed to send FCM push to user {user.name}: {e}")
