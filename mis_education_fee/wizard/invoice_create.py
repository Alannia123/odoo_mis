from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import get_lang


class InvCreation(models.TransientModel):
    _name = "inv.generate.wizard"
    _description = "invoice Generate Wizard"

    pre_amount = fields.Float('Previous Amount', readonly=True)
    current_amount = fields.Float('Current Amount', readonly=False)
    reason = fields.Char('Reason', required=True)


    def update_budget_amount(self):
        active_id = int(self._context.get('active_id'))
        budget_id = self.env['budget.master'].browse(active_id)
        budget_id.budget_amount = self.current_amount

        rev_len = self.env['budget.amount.revision'].search_count([('budget_id', '=', active_id)])
        budget_id.revision = rev_len + 1
        budget_id.budget_reason = self.reason
        bud_revision_id = self.env['budget.amount.revision'].create(
            {
                # 'name' : str(budget_id.name) +'_' + str(budget_id.revision),
                'project_id' : budget_id.project_id.id,
                'date' : fields.Datetime.now(),
                'pre_amount' : self.pre_amount,
                'current_amount' : self.current_amount,
                'revision' : budget_id.revision,
                'budget_id' : budget_id.id,
                'company_id' : budget_id.company_id.id,
                'reason' : self.reason,
            }
        )

