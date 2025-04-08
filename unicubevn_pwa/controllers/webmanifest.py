# -*- coding: utf-8 -*-
#   Copyright (c) by The Bean Family, 2023.
#   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#   These code are maintained by The Bean Family.

import base64
import json
import mimetypes

from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import ustr, file_open


class WebManifest(http.Controller):

    def _get_shortcuts(self):
        module_names = ['sales', 'point_of_sale', 'mail', 'crm', 'project', 'project_todo']
        try:
            module_ids = request.env['ir.module.module'].search([('state', '=', 'installed'), ('name', 'in', module_names)]) \
                                                        .sorted(key=lambda r: module_names.index(r["name"]))
        except AccessError:
            return []
        menu_roots = request.env['ir.ui.menu'].get_user_roots()
        datas = request.env['ir.model.data'].sudo().search([('model', '=', 'ir.ui.menu'),
                                                         ('res_id', 'in', menu_roots.ids),
                                                         ('module', 'in', module_names)])
        shortcuts = []
        for module in module_ids:
            data = datas.filtered(lambda res: res.module == module.name)
            if data:
                shortcuts.append({
                    'name': module.display_name,
                    'url': '/web#menu_id=%s' % data.mapped('res_id')[0],
                    'description': module.summary,
                    'icons': [{
                        'sizes': '100x100',
                        'src': module.icon,
                        'type': mimetypes.guess_type(module.icon)[0] or 'image/png'
                    }]
                })
        return shortcuts

    @http.route('/web/manifest.webmanifest', type='http', auth='public', methods=['GET'])
    def webmanifest(self):
        """ Returns a WebManifest describing the metadata associated with a web application.
        Using this metadata, user agents can provide developers with means to create user
        experiences that are more comparable to that of a native application.
        """
        web_app_name = request.env['ir.config_parameter'].sudo().get_param('web.web_app_name', 'Unicube n')
        web_app_shortname = request.env['ir.config_parameter'].sudo().get_param('web.web_app_short_name', 'Unicube s')
        background_color = request.env['ir.config_parameter'].sudo().get_param('web.web_app_bg_color', '#FFFFFF')
        theme_color = request.env['ir.config_parameter'].sudo().get_param('web.web_app_theme_color', '#FFFFFF')
        existing_attachment = (
            request.env["ir.attachment"].sudo().search([("url", "like", "/unicubevn_pwa/img/")])
        )
        print (existing_attachment)
        manifest = {
            "$schema": "https://json.schemastore.org/web-manifest-combined.json",
            'name': web_app_name,
            'short_name': web_app_shortname,
            'scope': '/web',
            'start_url': '/web',
            'background_color': background_color,
            'theme_color': theme_color,
            "orientation": "any",
            "display": "fullscreen",
            "display_override": [
                "fullscreen", "standalone"
            ],
            'prefer_related_applications': False,
            "categories": [
                "business",
                "food",
                "shopping"
            ],
            "description": "This is PWA for Business",
            "iarc_rating_id": "a",
            "screenshots": [
                {
                    "src": '/unicubevn_pwa/static/img/icon-512x512.png',
                    "sizes": "512x512",
                    "type": "image/png",
                    "form_factor": "wide"
                },
                {
                    "src": '/unicubevn_pwa/static/img/icon-512x512.png',
                    "sizes": "512x512",
                    "type": "image/png",
                }
            ],

        }
        # values = {
        #     "datas": icon,
        #     "db_datas": icon,
        #     "url": url,
        #     "name": url,
        #     "type": "binary",
        #     "mimetype": mimetype,
        # }
        if existing_attachment:
                for attachment in existing_attachment:
                    print(f'{attachment.url} - {attachment.mimetype}')
                    print(f"{attachment.name}")
                manifest['icons'] = [{
                    'src': f'{attachment.url}',
                    'sizes': f"{attachment.name}",
                    'type': f'{attachment.mimetype}',
                } for attachment in existing_attachment if attachment.name != 'default']
        else:
            icon_sizes = ['192x192', '512x512']
            # icon_path =
            manifest['icons'] = [{
                'src': '/unicubevn_pwa/static/img/icon-%s.png' % size,
                'sizes': size,
                'type': 'image/png',
            } for size in icon_sizes]
        manifest['shortcuts'] = self._get_shortcuts()
        body = json.dumps(manifest, default=ustr)
        response = request.make_response(body, [
            ('Content-Type', 'application/manifest+json'),
        ])
        return response

    @http.route('/web/service-worker.js', type='http', auth='public', methods=['GET'])
    def service_worker(self):
        response = request.make_response(
            self._get_service_worker_content(),
            [
                ('Content-Type', 'text/javascript'),
                ('Service-Worker-Allowed', '/web'),
            ]
        )
        return response

    def _get_service_worker_content(self):
        """ Returns a ServiceWorker javascript file scoped for the backend (aka. '/web')
        """

        with file_open('web/static/src/service_worker.js') as f:
            body = f.read()
            return body

    def _icon_path(self):
        return 'unicubevn_pwa/static/img/icon-192x192.png'

    @http.route('/web/offline', type='http', auth='public', methods=['GET'])
    def offline(self):
        """ Returns the offline page delivered by the service worker """
        return request.render('web.webclient_offline', {
            'odoo_icon': base64.b64encode(file_open(self._icon_path(), 'rb').read())
        })

    """Controller for handling push notifications using Firebase
        Cloud Messaging"""

    @http.route('/push_notification', type='http', auth="public",
                csrf=False)
    def get_registration_tokens(self, **post):
        """Handles registration tokens for push notifications.
         Create a new registration token if it doesn't already exist
        :param post: POST request data containing registration token.
        :type post: dict
       """
        user_notification = request.env['push.notification'].sudo().search(
            [('register_id', '=', post.get('name'))], limit=1)
        if not user_notification:
            request.env['push.notification'].sudo().create({
                'register_id': post.get('name'),
                'user_id': request.env.user.id
            })

    @http.route('/firebase_config_details', type='json', auth="public")
    def send_datas(self):
        """Sends Firebase configuration details.
        :return: JSON containing Firebase configuration details.
        :rtype: str"""
        if request.env.company and request.env.company.push_notification:
            return json.dumps({
                'vapid': request.env.company.vapid,
                'config': {
                    'apiKey': request.env.company.api_key,
                    'authDomain': request.env.company.auth_domain,
                    'projectId': request.env.company.project_id_firebase,
                    'storageBucket': request.env.company.storage_bucket,
                    'messagingSenderId': request.env.company.messaging_sender_id_firebase,
                    'appId': request.env.company.app_id_firebase,
                    'measurementId': request.env.company.measurement_id_firebase
                }
            })

    @http.route('/firebase_credentials', type="json", auth="public")
    def firebase_credentials(self, **kw):
        """ Retrieve Firebase credentials for the current company."""
        return {'id': request.env.company.id,
                'push_notification': request.env.company.push_notification}

    @http.route('/firebase-messaging-sw.js', type='http', auth="public")
    def firebase_http(self):
        """Returns the Firebase service worker script.
        :return: The Firebase service worker script.
        :rtype: str"""
        if request.env.company and request.env.company.push_notification:
            firebase_js = """
                this.addEventListener('fetch', function(e) {
                  e.respondWith(
                    caches.match(e.request).then(function(response) {
                      return response || fetch(e.request);
                    })
                  );
                });
                importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
                importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');
                var firebaseConfig = {
                    apiKey: '%s',
                    authDomain: '%s',
                    projectId: '%s',
                    storageBucket: '%s',
                    messagingSenderId: '%s',
                    appId: '%s',
                    measurementId: '%s',
                };
                firebase.initializeApp(firebaseConfig);
                const messaging = firebase.messaging();


                messaging.onBackgroundMessage(function(payload) {
                    console.log(
                        '[firebase-messaging-sw.js] Received background message ',
                        payload
                      );
                    const notificationTitle = "Background Message Title";
                    const notificationOptions = {
                        body: payload.notification.body,
                        icon:'/mail_push_notification/static/description/icon.png',
                    };
                    return self.registration.showNotification(
                        notificationTitle,
                        notificationOptions,
                    );
                });
                """ % (
                request.env.company.api_key, request.env.company.auth_domain,
                request.env.company.project_id_firebase,
                request.env.company.storage_bucket,
                request.env.company.messaging_sender_id_firebase,
                request.env.company.app_id_firebase,
                request.env.company.measurement_id_firebase)
        else:
            firebase_js = """
                    this.addEventListener('fetch', function(e) {
                      e.respondWith(
                        caches.match(e.request).then(function(response) {
                          return response || fetch(e.request);
                        })
                      );
                    });
                """
        return http.request.make_response(firebase_js, [
            ('Content-Type', 'text/javascript')])
