from odoo import models, fields, http
from odoo.http import request


# Backend Model
class SchoolMagazine(models.Model):
    _name = 'school.magazine'
    _description = 'School e-Magazine'

    name = fields.Char(string='Magazine Title', required=True)
    upload_date = fields.Date(string='Upload Date', default=fields.Date.today)
    pdf_file = fields.Binary(string='PDF File', required=True, attachment=True)
    teacher_id = fields.Many2one('res.users', string='Uploaded by', default=lambda self: self.env.user)


# Controller for Website Display
class SchoolMagazineController(http.Controller):
    @http.route('/e-magazine', type='http', auth='public', website=True)
    def list_magazines(self, **kwargs):
        magazines = request.env['school.magazine'].sudo().search([])
        return request.render('school_magazine.template_magazine_list', {'magazines': magazines})


# XML Website Template
xml_template = """
<odoo>
    <template id="template_magazine_list" name="Magazine List">
        <t t-call="website.layout">
            <div class="container">
                <h2 class="text-center">E-Magazines</h2>
                <div class="row">
                    <t t-foreach="magazines" t-as="magazine">
                        <div class="col-md-2 magazine-item">
                            <a t-att-href="'/e-magazine/view/%s' % magazine.id">
                                <div class="magazine-card">
                                    <h4 t-esc="magazine.name"/>
                                    <span t-esc="magazine.upload_date" class="text-muted"/>
                                </div>
                            </a>
                        </div>
                    </t>
                </div>
            </div>
            <style>
                .magazine-item { text-align: center; margin-bottom: 20px; }
                .magazine-card { padding: 15px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.3s; }
                .magazine-card:hover { transform: scale(1.05); }
            </style>
        </t>
    </template>
    
    
    
    <template id="template_magazine_view" name="Magazine View">
        <t t-call="website.layout">
            <div class="container">
                <h2 class="text-center" t-esc="magazine.name"/>
                <div class="text-center text-muted" t-esc="magazine.upload_date"/>
                <div class="pdf-container text-center">
                    <iframe t-att-src="'/web/content/%s/pdf_file' % magazine.id" width="100%" height="600px"></iframe>
                </div>
                <div class="text-center mt-3">
                    <a t-att-href="'/web/content/%s/pdf_file?download=true' % magazine.id" class="btn btn-primary">Download PDF</a>
                </div>
            </div>
            <style>
                .pdf-container { margin-top: 20px; }
            </style>
        </t>
    </template>
</odoo>
</odoo>
"""





