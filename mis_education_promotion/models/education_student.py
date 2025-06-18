# -*- coding: utf-8 -*-


from odoo import fields, models


class EducationStudent(models.Model):
    """ Inherits the model education.student to add the field final_result"""
    _inherit = 'education.student'

    final_result = fields.Selection([
        ('na', 'Not Applicable'),
        ('pass', 'Pass'),
        ('fail', 'Fail'), ],
        string="Final Result", default='na',
        help='Field to know the final result of the student.')


class EducationStudentFinalResult(models.Model):
    """
       Model to store final results of education students.
       """
    _name = 'education.student.final.result'
    _description = 'Student Final Result'
    _rec_name = 'student_id'

    student_id = fields.Many2one('education.student', string="Student",
                                 help='Reference to the student linked to this '
                                      'final result.')
    final_result = fields.Selection([
        ('na', 'Not Applicable'),
        ('pass', 'Pass'),
        ('fail', 'Fail'), ],
        string="Final Result", default='na',
        help="The overall outcome of the student's academic performance.")
    division_id = fields.Many2one('education.class.division', string="Class",
                                  help='Indicates the class division to which'
                                       ' the student belongs.')
    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Academic Year',
                                       help='Represents the academic year '
                                            'during which the final result '
                                            'was recorded.')
    closing_id = fields.Many2one('education.promotion',
                                 string='Academic Year',
                                 help='Identifies the academic year closure '
                                      'or promotion details.')
