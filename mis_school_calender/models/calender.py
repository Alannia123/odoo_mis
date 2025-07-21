from odoo import models, fields

class SchoolEvent(models.Model):
    _name = 'school.event'
    _description = 'School Events'

    name = fields.Char('Event Title', required=True)
    event_date = fields.Date('Date', required=True)
    cover_image = fields.Image('Cover Image')
    # description = fields.Text('Description')
    is_published = fields.Boolean('Publish on Website', default=False)
