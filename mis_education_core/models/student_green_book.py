from odoo import models, fields, api, _
import base64
from odoo.exceptions import UserError, ValidationError



class GreenBook(models.Model):
    _name = 'student.green.book'
    _description = 'Green Book Upload'
    _rec_name = 'student_id'

    student_id = fields.Many2one('education.student', 'Student', required=True)
    register_no = fields.Char(related= 'student_id.register_no' , string='Registration Number', required=True)
    image_1920 = fields.Image(string="Image", max_width=1920, max_height=1920)
    photo = fields.Binary('Photo', readonly=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    green_line_ids = fields.One2many('student.green.line', 'green_line_id', 'Green Lines')
    no_of_history = fields.Integer('No Of History', compute='_compute_no_of_history')

    @api.onchange('student_id')
    def _onchange_check_exist_student(self):
        if self.student_id:
            check_exist = self.env['student.green.book'].search([('student_id', '=', self.student_id.id)])
            if check_exist:
                raise ValidationError(_('The Selected Student Discipline History Already Created, Please Check from exist Disciplines'))

    @api.model
    def create(self, vals):
        res = super(GreenBook, self).create(vals)
        print('SSSSSSSSSSSSSSSS',res.student_id.partner_id)
        res.photo = res.student_id.partner_id.image_1920
        print('SSSSSSSSSSSSSSSS', res.photo)
        return res

    def _compute_no_of_history(self):
        for rec in self:
            rec.no_of_history = len(rec.green_line_ids)


class GreenBookline(models.Model):
    _name = 'student.green.line'
    _description = 'Green Book Line'

    green_line_id = fields.Many2one('student.green.book', 'Green Book')
    enter_date = fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    enter_remark = fields.Char(string='Remarks', required=True)
    file_name = fields.Char(string='File Name (Stored)')  # Optional, for storing original file name
    file_data = fields.Binary(string='File', required=False, attachment=True)



