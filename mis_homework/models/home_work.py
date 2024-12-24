from datetime import date

from odoo import models, fields, api, _



class StudentHomework(models.Model):
    _name = 'student.homework'
    _description = 'Student Homework'

    name = fields.Char(string="Homework Title", required=True, readonly=True, default='New' )
    description = fields.Text(string="Description")
    homework_date = fields.Date(string='Homework Date', default=fields.Date.today, readonly=True)
    class_div_id = fields.Many2one('education.class.division', 'Class', required=True, readonly=True)
    work_line_ids = fields.One2many('student.homework.line', 'work_id', string="Home Work")
    work_view_ids = fields.One2many('student.homework.view', 'work_id', string="Home Work")
    state = fields.Selection([('draft', 'Draft'), ('post', 'Posted')], 'State', default='draft')
    # homework_desc = fields.Html('Homeworks', readonly=True)

    # @api.model
    # def create(self, vals):
    #     res = super(StudentHomework, self).create(vals)
    #     res.name = str(res.class_div_id.name) + ' - (' + str(res.homework_date.strftime("%d-%m-%Y")) +')'
    #     res.description = res.name
    #     return res

    def generate_homework_template(self):
        today = date.today()
        all_class_ids = self.env['education.class.division'].search([])
        for clas_div in all_class_ids:
            temp_id = self.env['student.homework'].create({
                                                            'homework_date': today,
                                                            'class_div_id': clas_div.id,
                                                            'name': str(clas_div.name) + ' - (' + str(today.strftime("%d-%m-%Y")) +')',
                                                        })

    def action_create_to_student(self):
        print('SSSSSSSSSSSSSS')
        if self.work_view_ids:
            self.work_view_ids = [fields.Command.clear()]
        if self.work_line_ids:
            for work in self.work_line_ids:
                homework_desc = f"""
                                        <h1 style="color : red;">{work.subject_id.name}</h1><br/>
                                        <p style="color : green;"> {work.homework}. </p>
                                    """
                view_id = self.env['student.homework.view'].create({
                                                                    'work_id' : self.id,
                                                                    'work_view_attachment_ids' : work.work_attachment_ids.ids,
                                                                    })
                print('DDDDDDFFFFFFFFF00000000',view_id)
                if view_id:
                    view_id.homework_desc = f"""
                                        <h1>{work.subject_id.name}</h1><br/>
                                        <p> {work.homework}. </p>
                                    """
        self.state = 'post'

    def action_update_to_student(self):
        print('SSSSSSSSSSSSSS')

class StudentHomeworkLine(models.Model):
    _name = 'student.homework.line'
    _description = 'Student Homework Line'

    work_id = fields.Many2one('student.homework', string="Home Work")
    subject_id = fields.Many2one('education.subject', 'Subject', required=True)
    homework = fields.Char('Homework')
    work_attachment_ids = fields.Many2many(
        'ir.attachment', 'education_work_attach_rel',
        'work_id', 'work_attach', string="Attachment", copy=False,
        help='You can attach the copy of your document')

class StudentHomeworkLine(models.Model):
    _name = 'student.homework.view'
    _description = 'Student Homework View'

    work_id = fields.Many2one('student.homework', string="Home Work", readonly=True)
    homework_desc = fields.Html('Homeworks', readonly=True)
    work_view_attachment_ids = fields.Many2many(
        'ir.attachment', 'education_view_attach_rel',
        'stu_view_id', 'stu_work_attach', string="Attachment", copy=False,
        help='You can attach the copy of your document')

#
