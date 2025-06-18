# -*- coding: utf-8 -*-
# Copyright 2022 Bean Bakery
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import base64
import io
import sys

from PIL import Image

from odoo import _, api, exceptions, fields, models
from odoo.tools.mimetypes import guess_mimetype

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _pwa_icon_url_base = "/unicubevn_pwa/img/"

    pwa_name = fields.Char(
        "App Name", help="Name of the Progressive Web Application"
    )
    pwa_short_name = fields.Char(
        "Short Name",
        help="Short Name of the Progressive Web Application",
    )
    pwa_icon = fields.Binary("Icon", readonly=False)
    pwa_background_color = fields.Char("Background Color", default="#FFFFFF")
    pwa_theme_color = fields.Char("Theme Color", default="#FFFFFF")
    # pwa_serverkey=fields.Char("VAPID server key", default="BLTLn9JbyFqdnOvEBywwf0AuPB3tfHpypKGLEn8T_BLo5ATRcZLUeQPxOYuvMBXyET9vhNHtReE25gthqilx3dk")
    # pwa_secretkey=fields.Char("VAPID private key", default="yfuW0sZdT8CBvnZlOn_rj63F9plMF5cNPKS_LSFXd9o")
    push_notification = fields.Boolean(string='Enable Push Notification',
                                       help="Enable Web Push Notification",
                                       related='company_id.push_notification',
                                       readonly=False)
    server_key = fields.Char(string="Server Key",
                             help="Server Key of the firebase",
                             related='company_id.server_key', readonly=False)
    vapid = fields.Char(string="Vapid", help='VapId of the firebase',
                        related='company_id.vapid', readonly=False)
    api_key = fields.Char(string="Api Key",
                          help='Corresponding apiKey of firebase config',
                          related='company_id.api_key', readonly=False)
    auth_domain = fields.Char(string="Auth Domain",
                              help='Corresponding authDomain of firebase '
                                   'config',
                              related='company_id.auth_domain', readonly=False)
    project_id_firebase = fields.Char(string="Project Id",
                                      help='Corresponding projectId of '
                                           'firebase config',
                                      related='company_id.project_id_firebase',
                                      readonly=False)
    storage_bucket = fields.Char(string="Storage Bucket",
                                 help='Corresponding storageBucket of '
                                      'firebase config',
                                 related='company_id.storage_bucket',
                                 readonly=False)
    messaging_sender_id_firebase = fields.Char(string="Messaging Sender Id",
                                               help='Corresponding '
                                                    'messagingSenderId of '
                                                    'firebase config',
                                               related='company_id'
                                                       '.messaging_sender_id_firebase',
                                               readonly=False)
    app_id_firebase = fields.Char(string="App Id",
                                  help='Corresponding appId of firebase config',
                                  related='company_id.app_id_firebase',
                                  readonly=False)
    measurement_id_firebase = fields.Char(string="Measurement Id",
                                          help='Corresponding measurementId '
                                               'of firebase config',
                                          related='company_id'
                                                  '.measurement_id_firebase',
                                          readonly=False)

    def test_connection(self):
        """Test connection to firebase using the firebase credentials"""
        if self.env.company.push_notification:
            try:
                push_service = FCMNotification(
                    api_key=self.env.company.server_key)
                registration_ids = self.env['push.notification'].sudo().search(
                    [('user_id', '=', self.env.user.id)])
                push_service.notify_multiple_devices(
                    registration_ids=[registration_id.register_id for
                                      registration_id in registration_ids],
                    message_title='Test Connection',
                    message_body='Successfully',
                    extra_notification_kwargs={
                        'click_action': '/web'
                    })
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'success',
                        'message': _("Connection successfully established"),
                        'next': {
                            'type': 'ir.actions.client',
                            'tag': 'reload_context',
                        },
                    }
                }
            except:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'danger',
                        'message': _(
                            "Failed to connect with firebase"),
                        'next': {
                            'type': 'ir.actions.client',
                            'tag': 'reload_context',
                        },
                    }
                }

    @api.model
    def get_values(self):
        config_parameter_obj_sudo = self.env["ir.config_parameter"].sudo()
        res = super(ResConfigSettings, self).get_values()
        res["pwa_name"] = config_parameter_obj_sudo.get_param(
            "web.web_app_name", default="UniCube JSC"
        )
        res["pwa_short_name"] = config_parameter_obj_sudo.get_param(
            "web.web_app_short_name", default="UniCube"
        )
        pwa_icon_ir_attachment = (
            self.env["ir.attachment"]
            .sudo()
            .search([("url", "like", self._pwa_icon_url_base + ".")])
        )
        res["pwa_icon"] = (
            pwa_icon_ir_attachment.datas if pwa_icon_ir_attachment else False
        )
        res["pwa_background_color"] = config_parameter_obj_sudo.get_param(
            "web.web_app_bg_color", default="#FFFFFF"
        )
        res["pwa_theme_color"] = config_parameter_obj_sudo.get_param(
            "web.web_app_theme_color", default="#FFFFFF"
        )
        # res["pwa_serverkey"] = config_parameter_obj_sudo.get_param(
        #     "web.web_app_serverkey", default="BLTLn9JbyFqdnOvEBywwf0AuPB3tfHpypKGLEn8T_BLo5ATRcZLUeQPxOYuvMBXyET9vhNHtReE25gthqilx3dk"
        # )
        # res["pwa_secretkey"] = config_parameter_obj_sudo.get_param(
        #     "web.web_app_secretkey", default="yfuW0sZdT8CBvnZlOn_rj63F9plMF5cNPKS_LSFXd9o"
        # )
        return res

    def _unpack_icon(self, icon):
        # Wrap decoded_icon in BytesIO object
        decoded_icon = base64.b64decode(icon)
        icon_bytes = io.BytesIO(decoded_icon)
        return Image.open(icon_bytes)

    def _write_icon_to_attachment(self, extension, mimetype, size=None):
        url = self._pwa_icon_url_base + extension
        icon = self.pwa_icon
        name= 'default'
        # Resize image
        if size:
            image = self._unpack_icon(icon)
            resized_image = image.resize(size)
            icon_bytes_output = io.BytesIO()
            resized_image.save(icon_bytes_output, format=extension.lstrip(".").upper())
            icon = base64.b64encode(icon_bytes_output.getvalue())
            url = "{}icon-{}x{}{}".format(
                self._pwa_icon_url_base,
                str(size[0]),
                str(size[1]),
                extension,
            )
            name = f"{str(size[0])}x{str(size[1])}"
        # Retreive existing attachment
        existing_attachment = (
            self.env["ir.attachment"].sudo().search([("url", "like", url)])
        )
        # Write values to ir_attachment
        values = {
            "datas": icon,
            "db_datas": icon,
            "url": url,
            "name": name,
            "type": "binary",
            "mimetype": mimetype,
        }
        # Rewrite if exists, else create
        if existing_attachment:
            existing_attachment.sudo().write(values)
        else:
            self.env["ir.attachment"].sudo().create(values)

    @api.model
    def set_values(self):
        config_parameter_obj_sudo = self.env["ir.config_parameter"].sudo()
        res = super(ResConfigSettings, self).set_values()
        # config_parameter_obj_sudo.set_param("web.web_app_serverkey", self.pwa_serverkey)
        # config_parameter_obj_sudo.set_param("web.web_app_secretkey", self.pwa_secretkey)
        config_parameter_obj_sudo.set_param("web.web_app_name", self.pwa_name)
        config_parameter_obj_sudo.set_param(
            "web.web_app_short_name", self.pwa_short_name
        )
        config_parameter_obj_sudo.set_param(
            "web.web_app_bg_color", self.pwa_background_color
        )
        config_parameter_obj_sudo.set_param(
            "web.web_app_theme_color", self.pwa_theme_color
        )
        # Retrieve previous value for pwa_icon from ir_attachment
        pwa_icon_ir_attachments = (
            self.env["ir.attachment"]
            .sudo()
            .search([("url", "like", self._pwa_icon_url_base)])
        )
        # Delete or ignore if no icon provided
        if not self.pwa_icon:
            if pwa_icon_ir_attachments:
                pwa_icon_ir_attachments.unlink()
            return res
        # Fail if icon provided is larger than 2mb
        if sys.getsizeof(self.pwa_icon) > 2196608:
            raise exceptions.UserError(
                _("You can't upload a file with more than 2 MB.")
            )
        # Confirm if the pwa_icon binary content is an SVG or PNG
        # and process accordingly
        decoded_pwa_icon = base64.b64decode(self.pwa_icon)
        # Full mimetype detection
        pwa_icon_mimetype = guess_mimetype(decoded_pwa_icon)
        pwa_icon_extension = "." + pwa_icon_mimetype.split("/")[-1].split("+")[0]
        if not pwa_icon_mimetype.startswith(
            "image/svg"
        ) and not pwa_icon_mimetype.startswith("image/png"):
            raise exceptions.UserError(
                _("You can only upload SVG or PNG files. Found: %s.")
                % pwa_icon_mimetype
            )
        # Delete all previous records if we are writting new ones
        if pwa_icon_ir_attachments:
            pwa_icon_ir_attachments.unlink()
        self._write_icon_to_attachment(pwa_icon_extension, pwa_icon_mimetype)
        # write multiple sizes if not SVG
        if pwa_icon_extension != ".svg":
            # Fail if provided PNG is smaller than 512x512
            if self._unpack_icon(self.pwa_icon).size < (512, 512):
                raise exceptions.UserError(
                    _("You can only upload PNG files bigger than 512x512")
                )
            for size in [
                (128, 128),
                (144, 144),
                (152, 152),
                (192, 192),
                (256, 256),
                (512, 512),
            ]:
                self._write_icon_to_attachment(
                    pwa_icon_extension, pwa_icon_mimetype, size=size
                )
