# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint




class Members(models.Model):
    _name = 'school.members'
    _description = 'School Members'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    create_date = fields.Date(string='Create Date', default=fields.Date.today)
    member_line_ids = fields.One2many('school.members.line', 'member_id', 'Member Lines')

class MembersLine(models.Model):
    _name = 'school.members.line'
    _description = 'School Members Line'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"


    member_id = fields.Many2one('school.members', 'Members')
    name = fields.Char('Name', copy=False)
    desc = fields.Char('Desc', copy=False)
    designation = fields.Selection([('president', 'President'),('secretary', 'Secretary'),
                                    ('principal', 'Principal'),('manager', 'Manager')],'Designation', copy=False)
    image = fields.Image(string='Image', required=True, attachment=True)


