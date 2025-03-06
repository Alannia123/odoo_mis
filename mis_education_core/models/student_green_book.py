from odoo import models, fields

class GreenBook(models.Model):
    _name = 'student.green.book'
    _description = 'Green Book Upload'

    student_id = fields.Many2one('education.student', 'Student', required=True)
    class_div_id = fields.Many2one('education.class.division', 'Division', required=True)
    file_data = fields.Binary(string='File', required=True, attachment=True)
    file_name = fields.Char(string='File Name (Stored)')  # Optional, for storing original file name
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    remarks = fields.Char(string='Remarks', required=True)
