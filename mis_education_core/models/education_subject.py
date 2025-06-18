# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationSubject(models.Model):
    """Manages subjects of institute"""
    _name = 'education.subject'
    _description = 'Subject Details'

    name = fields.Char(string='Name', required=True,
                       help="Name of the Subject")
    type = fields.Selection([('lkg', 'LKG'),('ukg', 'UKG'), ('onetwo', '1-2 STD'), ('threefive', '3-5 STD'),
                             ('sixeight', '6-8 STD'), ('ninten', '9-10 STD')],
                            'Report Card', required=False)

    # is_language = fields.Boolean(string="Language",
    #                              help="Tick if this subject is a language")
    # is_lab = fields.Boolean(string="Lab", help="Tick if this subject is a Lab")
    # code = fields.Char(string="Code", help="Enter the Subject Code")
    # type = fields.Selection(
    #     [('compulsory', 'Compulsory'), ('elective', 'Elective')],
    #     string='Type', default="compulsory",
    #     help="Choose the type of the subject")
    # weightage = fields.Float(string='Weightage', default=1.0,
    #                          help="Enter the weightage for this subject")
    # description = fields.Text(string='Description',
    #                           help="Note about the subject")

    _sql_constraints = [
        ('code', 'unique(code)',
         "Another Subject already exists with this code!"),
    ]

    @api.constrains('weightage')
    def check_weightage(self):
        """Return warning if the weightage given is not a positive value"""
        for rec in self:
            if rec.weightage <= 0:
                raise ValidationError(_('Weightage must be Positive'))
