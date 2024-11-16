# -*- coding: utf-8 -*-

from odoo import fields, models


class DocumentDocument(models.Model):
    """For managing document type"""
    _name = 'document.document'
    _description = "Documents Type"

    name = fields.Char(string='Name', required=True,
                       help="Name of the document type")
    description = fields.Char(string='Description', help="Note about the type")
