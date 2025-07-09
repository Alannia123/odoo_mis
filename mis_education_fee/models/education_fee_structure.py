# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EducationFeeStructure(models.Model):
    """Creating model 'education.fee.structure'"""
    _name = 'education.fee.structure'
    _description = 'Education Fee Structure'
    _rec_name = 'fee_structure_name'

    @api.depends('fee_type_ids.fee_amount')
    def compute_total(self):
        self.amount_total = sum(line.fee_amount for line in self.fee_type_ids)

    company_currency_id = fields.Many2one('res.currency',
                                          string='Company Currency',
                                          compute='get_company_id',
                                          readonly=True, related_sudo=False,
                                          help='Company currency')
    fee_structure_name = fields.Char(string='Name', required=True,
                                     help='Name of fee structure')
    fee_type_ids = fields.One2many('education.fee.structure.lines',
                                   'fee_structure_id',
                                   string='Fee Types', help='Specify the '
                                                            'fee types.')
    comment = fields.Text(string='Additional Information',
                          help="Additional information regarding the fee"
                               " structure")
    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Academic Year', required=True,
                                       help='Mention the academic year.')
    expire = fields.Boolean(string='Expire',
                            help='Expired or not')
    amount_total = fields.Float(string='Amount',
                                currency_field='company_currency_id',
                                required=True, compute='compute_total',
                                help='Total amount')
    category_id = fields.Many2one('education.fee.category',
                                  string='Category', required=True,
                                  default=lambda self: self.env[
                                      'education.fee.category'].search([],
                                                                       limit=1),
                                  domain=[('fee_structure', '=', True)],
                                  help='Fees category.')
    journal_id = fields.Many2one('account.journal',
                                 string='Journal', required=True,
                                 help='Setting up of unique journal for each '
                                      'category help to distinguish '
                                      'account entries of each category ')
    payment_type = fields.Selection([
        ('onetime', 'One Time'),
        ('permonth', 'Per Month'),
        ('peryear', 'Per Year'),
        ], string='Payment Type', default='permonth',
        help='Payment type describe how much a payment effective.'
             ' Like, bus fee per month is 30 dollar, sports fee per '
             'year is 40 dollar, etc')


    def generate_inv_division_students(self):
        non_generate_div_ids = self.env['education.class.division'].search([('inv_generated', '=', False)])
        structure_id = self.env['education.fee.structure'].search([('payment_type', '=', 'peryear')], limit=1)
        for student in non_generate_div_ids[0].student_ids[:-3]:

            lines = []
            vals = {}
            for line in structure_id.fee_type_ids:
                name = line.fee_type_id.product_variant_id.description_sale
                if not name:
                    name = line.fee_type_id.product_variant_id.name
                fee_line = {
                    'price_unit': line.fee_amount,
                    'quantity': 1.00,
                    'product_id': line.fee_type_id.product_variant_id.id,
                    'name': name,
                    'account_id': structure_id.journal_id.default_account_id.id
                }
                lines.append((0, 0, fee_line))

            vals = {
                'student': student.id,  # Customer ID
                'class_division_id': student.class_division_id.id,  # Customer ID
                'register_no': student.register_no,  # Customer ID
                'partner_id': student.partner_id.id,  # Customer ID
                'fee_structure_id': structure_id.id,  # Customer ID
                'move_type': 'out_invoice',  # 'out_invoice' = customer invoice
                'invoice_date': fields.Date.today(),
                'journal_id': structure_id.journal_id.id,  # Typically "Customer Invoices" journal
                'invoice_line_ids': lines,
                }
            print('VALSSSSSSSSSSSSSSSS',vals)
            invoice = self.env['account.move'].create(vals)


