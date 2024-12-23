# -*- coding: utf-8 -*-

from odoo import fields, models


class HomeWorkWizard(models.TransientModel):
    _name = 'homework.entry'
    _description = 'Homework Entry'


    homework_date = fields.Date(string='Homework Date', default=fields.Date.today, readonly=True)
    class_div_id = fields.Many2one('education.class.division', 'Class', required=True)
    subject_id = fields.Many2one('education.subject', 'Subject', required=True)
    homework = fields.Char('Homework')
    image = fields.Binary('Image')


    def create_homework_entry(self):
        today_date = fields.Date.today,
        homework_temp_id = self.env['student.homework'].search([('class_div_id', '=', self.class_div_id.id), ('homework_date', '=', self.homework_date)], limit=1)
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA',homework_temp_id)
        work_line_id = self.env['student.homework.line'].create({
                                                                    'work_id': homework_temp_id.id,
                                                                    'subject_id': self.subject_id.id,
                                                                    'homework': self.homework,
                                                                })
        work_line_id.image = self.image
        homework_temp_id.action_create_to_student()


