# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HomeWorkWizard(models.TransientModel):
    _name = 'homework.entry'
    _description = 'Homework Entry'


    homework_date = fields.Date(string='Homework Date', default=fields.Date.today, readonly=True)
    class_div_id = fields.Many2one('education.class.division', 'Class', required=True)
    subject_id = fields.Many2one('education.subject', 'Subject', required=True)
    homework = fields.Char('Homework')
    image = fields.Binary('Image')


    def create_homework_entry(self):
        today_date = fields.Date.today
        work_line_id = False
        homework_temp_id = self.env['student.homework'].search([('class_div_id', '=', self.class_div_id.id), ('homework_date', '=', self.homework_date)], limit=1)
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA',homework_temp_id)
        if not homework_temp_id:
            raise ValidationError(_('Today HomeWork Template Not Created , Please check with Office...'))
        if homework_temp_id.work_line_ids:
            work_line_id = homework_temp_id.work_line_ids.filtered(lambda p: p.subject_id.id == self.subject_id.id)

        if not work_line_id:
            work_line_id = self.env['student.homework.line'].create({
                                                                    'work_id': homework_temp_id.id,
                                                                    'subject_id': self.subject_id.id,
                                                                    'homework': self.homework,
                                                                })
        else:
            work_line_id.homework = self.homework

        if self.image:
            exist_attach = self.env['ir.attachment'].search([('res_model', '=', 'student.homework.line'), ('res_id', '=', work_line_id.id)])
            if exist_attach:
                exist_attach.unlink()
            doc_attachment = self.env['ir.attachment'].sudo().create({
                'name': str(self.subject_id.name) + '-' + str(self.homework_date),
                'res_name': 'Document',
                'res_model': 'student.homework.line',
                'res_id': work_line_id.id if work_line_id else 0,
                'type': 'binary',
                'datas': self.image,
            })
            print('SSSSSSSSSSSSSSSS',doc_attachment)
            work_line_id.work_attachment_ids = doc_attachment.ids
            print('OOOOOOOOOOOOOOOOOOOOOOOOOOOO',work_line_id.work_attachment_ids)
        homework_temp_id.action_create_to_student()


