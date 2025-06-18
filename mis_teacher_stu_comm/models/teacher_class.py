# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint


class TeacherParentClass(models.Model):
    _name = 'teacher.class.parent'
    _description = "Class To Parent Communication"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char('Name', required=False, readonly=True, tracking=True)
    create_date = fields.Date('Date', default=lambda self: fields.Datetime.now(), tracking=True, readonly=True)
    class_div_id = fields.Many2one('education.class.division', 'Division', tracking=True, required=True)
    faculty_id = fields.Many2one('education.faculty', 'Faculty', tracking=True, required=True)
    desc = fields.Text('Desc', copy=False, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                                        default='draft', string="State", help="Stages of attendance" , tracking=True)
    faculty_ids = fields.Many2many('education.faculty', 'comm_fac_rel', 'comm_val', 'Faculties')

    @api.onchange('class_div_id')
    def _onchange_div_id(self):
        self.faculty_ids = False
        faculty_ids = []
        if self.class_div_id:
            self.faculty_ids = self.class_div_id.class_id.subject_ids.mapped('faculty_ids').ids


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'name' not in vals or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('teacher.class.parent') or _('New')
        return super().create(vals_list)


    def action_assign_to_class(self):
        return self.write({"state": "done"})

