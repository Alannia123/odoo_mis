from odoo import api, fields, models, modules


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    login_background_image = fields.Binary(
        string="Image", help='Select Background Image For Login Page')
    background_color = fields.Char(
        string="Background Color", config_parameter='advance_login_form.background_color', help="Select Background Color for Login Page")
    text_color = fields.Char(
        string="Text Color", config_parameter='advance_login_form.text_color', help="Select Text Color for Login Page")
    button_color = fields.Char(
        string="Button Color", config_parameter='advance_login_form.button_color', help="Select Button Color for Login Page")
    button_hover_color = fields.Char(
        string="Button Hover Color", config_parameter='advance_login_form.button_hover_color', help="Select Hover Color for Button")

    alignment = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right'),
        ('center', 'Center'),
    ], string='Alignment', default='center', config_parameter='advance_login_form.alignment', help='Select Background Theme')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            login_background_image=self.env['ir.config_parameter'].sudo(
            ).get_param('advance_login_form.login_background_image')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        set_login_background_image = self.login_background_image or False
        param.set_param('advance_login_form.login_background_image',
                        set_login_background_image)
