from odoo import models, fields



class StudentHomework(models.Model):
    _name = 'student.homework'
    _description = 'Student Homework'

    name = fields.Char(string="Homework Title", required=True)
    description = fields.Text(string="Description")
    student_id = fields.Many2one('res.partner', string="Student", domain=[('is_student', '=', True)])
    subject = fields.Char(string="Subject")
    due_date = fields.Date(string="Due Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
    ], string="Status", default='draft')
