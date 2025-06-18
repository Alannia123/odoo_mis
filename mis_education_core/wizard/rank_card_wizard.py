# -*- coding: utf-8 -*-

from odoo import fields, models


class RankCard(models.TransientModel):
    _name = 'rank.wizard'
    _description = 'Rank Card'


    class_div_id = fields.Many2one('education.class.division', string='Select Class', required=True)


    def action_generate_pdf(self):
        data = {
            'model': self.class_div_id.id,
        }
        return self.env.ref('mis_education_core.action_generate_rank_card').report_action(self.class_div_id.id)
