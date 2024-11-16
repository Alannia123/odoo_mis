# -*- coding: utf-8 -*-

import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationApplication(models.Model):
    """Manages student application and its verification"""
    _name = 'education.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Applications for the admission'
    _order = 'id desc'

    _sql_constraints = [
        ('aadhar_no', 'UNIQUE(aadhar_no)',
         "This Aadhar Number is already associated with another student.")
    ]


    @api.model
    def create(self, vals):
        aadhaar_no = vals.get('aadhar_no', '')

        if not re.match(r'^\d{12}$', aadhaar_no):
            raise ValidationError("Aadhaar number must be a 12-digit number.")

        # Check for uniqueness of Aadhaar number
        existing_record = self.search([('aadhar_no', '=', aadhaar_no)], limit=1)
        if existing_record:
            raise ValidationError("This Aadhar Number is already associated with another student.")
        res = super(EducationApplication, self).create(vals)
        res.name = self.env['ir.sequence'].next_by_code('education.application')
        return res

    def unlink(self):
        """Return warning if the application is not in the reject state"""
        for rec in self:
            if rec.state != 'reject':
                raise ValidationError(
                    _("Application can only be deleted after rejecting it"))

    def action_send_to_verify(self):
        """Button action for sending the application for the verification"""
        for rec in self:
            document_ids = self.env['education.document'].search(
                [('application_ref_id', '=', rec.id)])
            if not document_ids:
                raise ValidationError(_('No Documents provided'))
            rec.write({
                'state': 'verification'
            })

    def action_create_student(self):
        """Create student from the application
            and data and return the student"""
        for rec in self:
            values = {
                'name': rec.first_name,
                'last_name': rec.last_name,
                'middle_name': rec.middle_name,
                'application_id': rec.id,
                'father_name': rec.father_name,
                'mother_name': rec.mother_name,
                'guardian_id': rec.guardian_id.id,
                'street': rec.street,
                'street2': rec.street2,
                'city': rec.city,
                'state_id': rec.state_id.id,
                'country_id': rec.country_id.id,
                'zip': rec.zip,
                'is_same_address': rec.is_same_address,
                'per_street': rec.per_street,
                'per_street2': rec.per_street2,
                'per_city': rec.per_city,
                'per_state_id': rec.per_state_id.id,
                'per_country_id': rec.per_country_id.id,
                'per_zip': rec.per_zip,
                'gender': rec.gender,
                'date_of_birth': rec.date_of_birth,
                'blood_group': rec.blood_group,
                'nationality_id': rec.nationality_id.id,
                'email': rec.email,
                'mobile': rec.mobile,
                'phone': rec.phone,
                'image_1920': rec.image,
                'is_student': True,
                'medium_id': rec.medium_id.id,
                'religion': rec.religion,
                'caste': rec.caste,
                'sec_lang_id': rec.sec_lang_id.id,
                'mother_tongue': rec.mother_tongue,
                'admission_class_id': rec.admission_class_id.id,
                'company_id': rec.company_id.id,
            }
            if not rec.is_same_address:
                pass
            else:
                values.update({
                    'per_street': rec.street,
                    'per_street2': rec.street2,
                    'per_city': rec.city,
                    'per_state_id': rec.state_id.id,
                    'per_country_id': rec.country_id.id,
                    'per_zip': rec.zip,
                })

            student = self.env['education.student'].create(values)
            rec.write({
                'state': 'done'
            })
            return {
                'name': _('Student'),
                'view_mode': 'form',
                'res_model': 'education.student',
                'type': 'ir.actions.act_window',
                'res_id': student.id,
                'context': self.env.context
            }

    def reject_application(self):
        """Rejecting the student application for admission"""
        for rec in self:
            rec.write({
                'state': 'reject'
            })

    def action_application_verify(self):
        """Verifying the student application. Return warning if no Documents
         provided or if the provided documents are not in done state"""
        for rec in self:
            document_ids = self.env['education.document'].search(
                [('application_ref_id', '=', rec.id)])
            if document_ids:
                doc_status = document_ids.mapped('state')
                if all(state in ('done', 'returned') for state in doc_status):
                    rec.write({
                        'verified_by_id': self.env.uid,
                        'state': 'approve'
                    })
                else:
                    raise ValidationError(
                        _('All Documents are not Verified Yet, '
                          'Please complete the verification'))

            else:
                raise ValidationError(_('No Documents provided'))

    def _compute_document_count(self):
        """Return the count of the documents provided"""
        for rec in self:
            document_ids = self.env['education.document'].search(
                [('application_ref_id', '=', rec.id)])
            rec.document_count = len(document_ids)

    def action_document_view(self):
        """Return the list of documents provided along with this application"""
        self.ensure_one()
        domain = [
            ('application_ref_id', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'education.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create">
                               Click to Create for New Documents
                            </p>'''),
            'limit': 80,
            'context': {'default_application_ref_id': self.id}
        }

    def action_re_request(self):
        """Reapply rejected student application"""
        for rec in self:
            rec.write({
                'state': 'draft'
            })

    first_name = fields.Char(string='Name', required=True,
                             help="Enter First name of Student")
    last_name = fields.Char(string='Last Name',
                            help="Enter Last name of Student")
    exact_age_april = fields.Char('Exact Age(as on April 1st)')
    image = fields.Binary(string='Image',
                          attachment=True,
                          help="Provide the image of the Student")
    academic_year_id = fields.Many2one(
        'education.academic.year',
        string='Academic Year',
        help="Choose Academic year for which the admission is choosing")
    mother_tongue = fields.Char(string="Mother Tongue",
                                required=True,
                                help="Enter Student's Mother Tongue")
    admission_class_id = fields.Many2one(
        'education.class', string="Class",
        required=True, help="Enter Class to which the admission is seeking")
    admission_date = fields.Datetime(string='Admission Date',
                                     default=fields.Datetime.now,
                                     required=True, help="Date of admission")
    name = fields.Char(string='Application  No', readonly=True,
                        copy=False,
                       help="Application number of admission")
    aadhar_no = fields.Char('Adhar Number', required=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id,
                                 help="Current Company")
    email = fields.Char(string="Email", required=False,
                        help="Enter E-mail id for contact purpose")
    phone = fields.Char(string="Phone", copy=False,
                        help="Enter Phone no. for contact purpose")
    mobile = fields.Char(string="Mobile(WhatsApp", required=True,
                         help="Enter Mobile num for contact purpose")
    street = fields.Char(string='Street', help="Enter the street")
    street2 = fields.Char(string='Street2', help="Enter the street2")
    zip = fields.Char(change_default=True, string='ZIP code',
                      help="Enter the Zip Code")
    city = fields.Char(string='City', help="Enter the City name")
    state_id = fields.Many2one("res.country.state", string='State',
                               ondelete='restrict',
                               help="Select the State where you are from")
    country_id = fields.Many2one('res.country', string='Country',
                                 ondelete='restrict',
                                 help="Select the Country")
    is_same_address = fields.Boolean(
        string="Permanent Address same as above",
        default=True,
        help="Tick the field if the Present and permanent address is same")
    per_street = fields.Char(string='Street', help="Enter the street")
    per_street2 = fields.Char(string='Street2', help="Enter the street2")
    per_zip = fields.Char(change_default=True, string='ZIP code',
                          help="Enter the Zip Code")
    per_city = fields.Char(string='City', help="Enter the City name")
    per_state_id = fields.Many2one("res.country.state",
                                   string='State', ondelete='restrict',
                                   help="Select the State where you are from")
    per_country_id = fields.Many2one('res.country',
                                     string='Country', ondelete='restrict',
                                     help="Select the Country")
    date_of_birth = fields.Date(string="Date of Birth", required=True,
                                help="Enter your DOB")
    guardian_id = fields.Many2one('res.partner',
                                  string="Guardian", required=False,
                                  domain=[('is_parent', '=', True)],
                                  help="Tell us who will take care of you")
    description = fields.Text(string="Note",
                              help="Description about the admission")
    father_name = fields.Char(string="Father",
                              help="Proud to say my father is")
    father_qualify = fields.Char(string="Father's Qualification", required=False)
    father_occupation = fields.Char(string="Father's Occupation", required=False)
    mother_name = fields.Char(string="Mother", help="My mother's name is")
    mother_qualify = fields.Char(string="Mother's Qualification", required=False)
    mother_occupation = fields.Char(string="Mother's Occupation", required=False)
    religion = fields.Char(string="Religion",
                           help="My Religion is ")
    caste = fields.Char(string="Caste",
                        help="My Caste is ")
    class_division_id = fields.Many2one('education.class.division',
                                        string="Class",
                                        help="Admission taking class")
    active = fields.Boolean(string='Active', default=True,
                            help="To archive the admission form")
    document_count = fields.Integer(compute='_compute_document_count',
                                    string='# Documents',
                                    help="Documents of student")
    verified_by_id = fields.Many2one('res.users',
                                     string='Verified by',
                                     help="The Document is verified by")
    reject_reason_id = fields.Many2one('application.reject.reason',
                                       string='Reject Reason',
                                       help="Application is rejected because")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender', required=True, default='male',
        track_visibility='onchange', help="Your Gender is")
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')],
        string='Blood Group', required=True, default='a+',
        track_visibility='onchange', help="Your Blood Group is")
    state = fields.Selection([('draft', 'Draft'),
                              ('verification', 'Verify'),
                              ('approve', 'Approve'),
                              ('reject', 'Rejected'), ('done', 'Done')],
                             string='State', required=True, default='draft',
                             track_visibility='onchange', copy=False,
                             help="Stages of admission")
    exist_sis_bro_info = fields.Boolean('Student has a sister/brother in this school(not cousin/relatives)')
    exist_name = fields.Char('Name')
    exist_class = fields.Many2one('education.class', 'Class')
    exist_section = fields.Many2one('education.division', 'Section')
    special_concern = fields.Char('Special Concern regarding Child')
