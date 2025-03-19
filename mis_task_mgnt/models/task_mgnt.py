# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint


class MisTask(models.Model):
    _name = 'task.management'
    _description = "MIS Task Management"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char('Name', required=False, readonly=True, tracking=True)
    create_date = fields.Date('Date', default=lambda self: fields.Datetime.now(), tracking=True, readonly=True)
    scheduled_date = fields.Date('Completion Date', default=lambda self: fields.Datetime.now(), tracking=True)
    user_id = fields.Many2one('res.users', 'Faculty', tracking=True)
    task_desc = fields.Text('Task Desc', copy=False, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('done', 'Completed')],
                                        default='draft', string="State", help="Stages of attendance" , tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'name' not in vals or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('task.management') or _('New')
        return super().create(vals_list)


    def action_assign_to_faculty(self):
        return self.write({"state": "assigned"})

    def accept_task_by_faculty(self):
        return self.write({"state": "in_progress"})

    def complete_task_by_faculty(self):
        return self.write({"state": "done"})

    def reset_to_draft(self):
        return self.write({"state": "draft"})