# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _


class EducationDocument(models.Model):
    """For managing student document details and verification"""
    _name = 'education.document'
    _description = "Student Documents"
    _inherit = ['mail.thread']

    @api.model
    def create(self, vals):
        """Overriding the create method to assign
        the sequence for newly creating records"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'education.document') or _('New')
        res = super(EducationDocument, self).create(vals)
        return res

    def action_verify_document(self):
        """Return the state to done if the documents are perfect"""
        for rec in self:
            rec.write({
                'verified_by_id': self.env.uid,
                'verified_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                'state': 'done'
            })

    def action_need_correction(self):
        """Return the state to correction if the documents are not perfect"""
        for rec in self:
            rec.write({
                'state': 'correction'
            })

    def action_hard_copy_returned(self):
        """Records who return the documents and when is it returned"""
        for rec in self:
            if rec.state == 'done':
                rec.write({
                    'state': 'returned',
                    'returned_by_id': self.env.uid,
                    'returned_date': datetime.datetime.now().strftime(
                        "%Y-%m-%d")
                })

    name = fields.Char(string='Serial Number', copy=False,
                       help="Serial number of document",
                       default=lambda self: _('New'))
    document_type_id = fields.Many2one('document.document',
                                       string='Document Type', required=False,
                                       help="Choose the type of the Document")
    birth_adaher = fields.Selection([('aadhar', 'AADHAR'), ('birth', 'B.CERTIFICATE')])
    description = fields.Text(string='Description', copy=False,
                              help="Enter a description about the document")
    has_hard_copy = fields.Boolean(
        string="Hard copy Received",
        help="Tick the field if the hard copy is provided")
    location_id = fields.Many2one(
        'stock.location', 'Location',
        domain="[('usage', '=', 'internal')]",
        help="Location where which the hard copy is stored")
    location_note = fields.Char(string="Location Note",
                                help="Enter some notes about the location")
    submitted_date = fields.Date(string="Submitted Date",
                                 default=fields.Date.today(),
                                 help="Documents are submitted on")
    received_by_id = fields.Many2one('hr.employee',
                                     string="Received By",
                                     help="The Documents are received by")
    returned_by_id = fields.Many2one('hr.employee',
                                     string="Returned By",
                                     help="The Documents are returned by")
    verified_date = fields.Date(string="Verified Date",
                                help="Date at the verification is done")
    returned_date = fields.Date(string="Returned Date", help="Returning date")
    responsible_verified_id = fields.Many2one('hr.employee',
                                              string="Responsible",
                                              help="Responsible person to "
                                                   "verify the document")
    responsible_returned_id = fields.Many2one('hr.employee',
                                              string="Responsible",
                                              help="Responsible person to "
                                                   "verify the returned "
                                                   "document")
    verified_by_id = fields.Many2one('res.users',
                                     string='Verified by',
                                     help="Document is verified by the user")
    application_ref_id = fields.Many2one('education.application',
                                         copy=False, string="Application Ref",
                                         help="Application reference "
                                              "of document")

    doc_attachment_ids = fields.Many2many(
        'ir.attachment', 'education_doc_attach_rel',
        'doc_id', 'attach_id3', string="Attachment", copy=False,
        help='You can attach the copy of your document')
    state = fields.Selection(
        [('draft', 'Draft'), ('correction', 'Correction'),
         ('done', 'Done'), ('returned', 'Returned')], string='State',
        required=True, default='draft',
        track_visibility='onchange', help="Stages of document ")
