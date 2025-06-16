# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Account(models.Model):
    """The Dashboard model used to build the all details of the
    Educational system"""
    _inherit = "account.move"
    _description = "Account Move"

    @api.model
    def get_fees_paid_unpaid_result(self, *args):
        """ Function to get exam results in each academic year """
        print('DDDDDWWWWWWWWWWWWWWWSSSSSSSSSSSS@@@@@@@-------------',self, args)
        academic_exam_result_dict = {}
        academic_pass_count = self.env['results.subject.line'].search_count(
            [('academic_year_id.id', '=', *args), ('pass_or_fail', '=', True)])
        academic_fail_count = self.env['results.subject.line'].search_count(
            [('academic_year_id.id', '=', *args), ('pass_or_fail', '=', False)])
        academic_exam_result_dict.update(
            {'Pass': academic_pass_count, 'Fail': academic_fail_count})
        return academic_exam_result_dict