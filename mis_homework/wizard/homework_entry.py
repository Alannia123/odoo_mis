# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
import base64


class HomeWorkWizard(models.TransientModel):
    _name = 'homework.entry'
    _description = 'Homework Entry'


    homework_date = fields.Date(string='Homework Date', default=fields.Date.today, readonly=True)
    class_div_id = fields.Many2one('education.class.division', 'Division', required=True)
    subject_id = fields.Many2one('education.subject', 'Subject', required=True )
    domain_subjects = fields.Many2many('education.subject', 'edu_sub_rel', 'edu_subject_id', 'subject_id', 'Subjects')
    homework = fields.Text('Homework')
    file_name = fields.Char('File Name')
    file_upload = fields.Binary('File Upload')
    erase_exist = fields.Boolean('Erase Existing Homework')


    @api.onchange('file_upload')
    def _check_pdf(self):
        """ Validate that the uploaded file is a PDF """
        if self.file_upload:
            decoded_file = base64.b64decode(self.file_upload)  # Decode the binary file
            if not decoded_file.startswith(b"%PDF-"):  # Check PDF magic number
                raise ValidationError("Only PDF files are allowed!")


    def create_homework_entry(self):
        work_line_id = False
        homework_id = False
        today = date.today()
        homework_id = self.env['student.homework'].search([('class_div_id', '=', self.class_div_id.id), ('homework_date', '=', self.homework_date)])
        if homework_id:
            work_line_id = homework_id.work_line_ids.filtered(lambda p: p.subject_id.id == self.subject_id.id)
            if work_line_id and not self.erase_exist:
                work_line_id.homework = work_line_id.homework + ' ' + self.homework
            if work_line_id and self.erase_exist:
                work_line_id.homework = self.homework
            else:
                work_line_id = self.env['student.homework.line'].create({
                    'work_id': homework_id.id,
                    'subject_id': self.subject_id.id,
                    'homework': self.homework,
                    'uploaded_by': self.env.user.id,
                })
        else:
            homework_id = self.env['student.homework'].create({
                                'homework_date': today,
                                'class_div_id': self.class_div_id.id,
                                'name': str(self.class_div_id.name) + ' - (' + str(today.strftime("%d-%m-%Y")) + ')',
                            })
            work_line_id = self.env['student.homework.line'].create({
                'work_id': homework_id.id,
                'subject_id': self.subject_id.id,
                'homework': self.homework,
                'uploaded_by': self.env.user.id
            })
        if self.file_upload:
            exist_attach = self.env['ir.attachment'].search([('res_model', '=', 'student.homework.line'), ('res_id', '=', work_line_id.id)])
            if exist_attach:
                exist_attach.unlink()
            doc_attachment = self.env['ir.attachment'].sudo().create({
                'name': self.file_name,
                'res_name': 'Homework',
                'res_model': 'student.homework.line',
                'res_id': work_line_id.id if work_line_id else 0,
                'type': 'binary',
                'datas': self.file_upload,
            })
            work_line_id.attachment_id = doc_attachment.id
        return {
            'name': _('Home Work'),
            'view_mode': 'form',
            'res_model': 'student.homework',
            'type': 'ir.actions.act_window',
            'res_id': homework_id.id,
            # 'context': self.env.context
        }

    @api.onchange('class_div_id', 'subject_id')
    def domain_subject_ids(self):
        # if not self.class_div_id:
        #     raise ValidationError(_( "Please enter Division First...!" ))
        if self.class_div_id:
            self.domain_subjects = self.class_div_id.class_id.subject_ids.mapped('subject_id').ids
        else:
            self.domain_subjects = False



