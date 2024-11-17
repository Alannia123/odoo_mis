# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo import _
from odoo.http import request, route, Controller, content_disposition
import io



class OnlineAdmission(http.Controller):
    """Controller for taking online admission"""

    @http.route('/university', type='http', auth='public', website=True)
    def university_contact_us(self):
        """To redirect to contact page."""
        return request.render('mis_website.university')

    @http.route('/call', type='http', auth='public', website=True)
    def about_contact_us(self):
        """To redirect to contact page."""
        return request.render('mis_website.custom_website_page')

    @http.route('/library', type='http', auth='public', website=True)
    def about_contact_us(self):
        """To redirect to contact page."""
        return request.render('mis_website.custom_library')

    @http.route('/applyonline', type='http', auth='public', website=True)
    def online_admission(self):
        """To pass certain default field values
                                  to the website registration form."""
        vals = {
            'classes': request.env['education.class'].sudo().search([('open_addmission', '=', True)]),
            'exist_classes': request.env['education.class'].sudo().search([]),
            'sections': request.env['education.division'].sudo().search([]),
        }
        return request.render('mis_website.online_admission', vals)

    @http.route('/admission/submit', type='http', auth='public',   website=True)
    def register_admission(self, **post):
        """ This will create a new student application with the values."""
        # # uploaded_photo = post.get('photo')
        # upload_birth_certi = post.get('birth_certi')
        # upload_adhar = post.get('adhar')
        # print('DDDDDDDDDDDDDDDDD',upload_birth_certi)
        # # if uploaded_photo:
        # #     file_content = uploaded_photo.read()
        # #     file_size = len(file_content)  # in bytes
        # #     file_size_kb = file_size / 1024
        # #     max_size = 1 * 1024 * 1024  # 5 MB in bytes
        # #     print('SSSSSSSSSSSSSSSSSfile_size_kbfile_size_kb', file_size_kb)
        # #     print('SSSSSSSSSSSSSSSSSfile_size_kbfile_size_kbTYPE', type(file_content))
        # #     print('DSSSSSSSSSSSSSSSmax_size', max_size)
        # #     if file_size > max_size:
        # #         return "Your Uploaded Student Photo size file exceeding 1MB. Please Update within 1MB."
        #
        # if upload_birth_certi:
        #     file_content_birth = upload_birth_certi.read()
        #     file_size_birth = len(file_content_birth)  # in bytes
        #     file_size_kb_birth = file_size_birth / 1024
        #     print('SSSSSSSSSSSSSSSSS',file_size_kb_birth)
        #     birth_max_size = 2 * 1024 * 1024  # 5 MB in bytes
        #     print('DSSSSSSSSSSSSSSS',birth_max_size)
        #     if file_size_birth > birth_max_size:
        #         return "Your Uploaded Student Birth Cretificate file size exceeding 2MB. Please Update within 2MB."
        #
        # if upload_adhar:
        #     file_content_adhar = upload_adhar.read()
        #     file_size_aadhar = len(file_content_adhar)  # in bytes
        #     file_size_kb_adhar = file_size_aadhar / 1024
        #     adhar_max_size = 2 * 1024 * 1024  # 5 MB in bytes
        #     if file_size_aadhar > adhar_max_size:
        #         return "Your Uploaded Student Aadhar file size exceeding 2MB. Please Update within 2MB."
        exist_student = False
        print('PJO________________',post.get('photo'))
        if post:
            academic_year_id = request.env['education.academic.year'].sudo().search([('next_acdemic_year', '=', True)], limit=1)
            print('ACSDBDGHGDHGDH',academic_year_id)
            if post.get('student_have_brother_sister') == 'no':
                exist_student = False
            else:
                exist_student = True
            application = request.env['education.application'].sudo().create({
                'admission_date': datetime.now(),
                'academic_year_id': academic_year_id.id,
                'first_name': post.get('first_name'),
                'last_name': post.get('last_name'),
                'date_of_birth': post.get('date'),
                'religion': post.get('religion'),
                'caste': post.get('caste'),
                'exact_age_april': post.get('exact_age'),
                'gender': post.get('gender'),
                'admission_class_id': post.get('class_of_addmision'),
                'mother_tongue': post.get('mother_tongue'),
                'father_name': post.get('father'),
                'mother_name': post.get('mother'),
                'father_qualify': post.get('father_qualify'),
                'mother_qualify': post.get('mother_qualify'),
                'father_occupation': post.get('father_occupation'),
                'mother_occupation': post.get('mother_occupation'),
                'street': post.get('street_1'),
                'street2': post.get('street_2'),
                'city': post.get('street_city'),
                'zip': post.get('street_zip'),
                'mobile': post.get('mobile_whats'),
                'phone': post.get('alternate_phone'),
                'aadhar_no': post.get('aahar_no'),
                'blood_group': post.get('blood_group'),
                # 'exist_sis_bro_info': exist_student,
                # 'exist_name': post.get('already_student_name'),
                # 'exist_class': post.get('already_student_class'),
                # 'exist_section': post.get('already_student_section'),
                'special_concern': post.get('special_concern'),
                'per_street': post.get('communication_address'),
                'image': base64.b64encode((post.get('photo')).read()),
                # 'image': io.BytesIO((post.get('photo')).read()),
            })
            doc_attachment = request.env['ir.attachment'].sudo().create({
                'name': post.get('birth_certi').filename,
                'res_name': 'Document',
                'type': 'binary',
                'datas': base64.encodebytes((post.get('birth_certi')).read()),
            })
            adhar_doc_attachment = request.env['ir.attachment'].sudo().create({
                'name': post.get('adhar').filename,
                'res_name': 'Aadhar',
                'type': 'binary',
                'datas': base64.encodebytes((post.get('adhar')).read()),
            })
            request.env['education.document'].sudo().create({
                # 'document_type_id': post.get('doc_type'),
                'doc_attachment_ids': doc_attachment,
                'birth_adaher': 'birth',
                'application_ref_id': application.id
            })
            request.env['education.document'].sudo().create({
                # 'document_type_id': post.get('doc_type'),
                'doc_attachment_ids': adhar_doc_attachment,
                'birth_adaher': 'aadhar',
                'application_ref_id': application.id
            })
            if application:
                application.admission_class_id.get_filled_seats_on_class()
            # users = request.env.ref('mis_education_core.group_education_principal').users
            # for user in users:
            #     application.activity_schedule('mis_education_core.new_addmission_application_receiving_activity',
            #                            user_id=user.id, note=f'New Admission Enquiry  {application.name}')
            # users = request.env.ref('mis_education_core.group_education_office_admin').users
            # for user in users:
            #     application.activity_schedule('mis_education_core.new_addmission_application_receiving_activity',
            #                            user_id=user.id, note=f'New Admission Enquiry  {application.name}')

            # return request.env.ref('mis_education_core.action_student_application_report').sudo().report_action(application.id)
        return request.render( "mis_website.submit_admission", {'application' : application})


    @http.route(['/report/pdf/<int:id>'], type='http', auth="public", website=True)
    def download_pdf(self, id, **kwargs):
        report = request.env.ref('mis_education_core.action_student_application_report')
        print('DDDDDDDFFFFFFFFFFF',id)
        application_id = request.env['education.application'].sudo().browse(id)
        pdf_content, dummy = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
            report, id, data={

            })
        report_name = _('Online Application Form %s', application_id.name)
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', content_disposition(report_name + '.pdf'))
        ]

        return request.make_response(pdf_content, headers=pdfhttpheaders)



    # sample

    # resume_type_education = request.env.ref('hr_skills.resume_type_education', raise_if_not_found=False)
    # skill_type_language = request.env.ref('hr_skills.hr_skill_type_lang', raise_if_not_found=False)
    #
    #
    #
    # report = request.env.ref('hr_skills.action_report_employee_cv', False)
    #
    # pdf_content, dummy = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
    #     report, employees.ids, data={
    #         'color_primary': color_primary,
    #         'color_secondary': color_secondary,
    #         'resume_type_education': resume_type_education,
    #         'skill_type_language': skill_type_language,
    #         'show_skills': 'show_skills' in post,
    #         'show_contact': 'show_contact' in post,
    #         'show_others': 'show_others' in post,
    #     })
    #
    # if len(employees) == 1:
    #     report_name = _('Resume %s', employees.name)
    # else:
    #     report_name = _('Resumes')
    #
    # pdfhttpheaders = [
    #     ('Content-Type', 'application/pdf'),
    #     ('Content-Length', len(pdf_content)),
    #     ('Content-Disposition', content_disposition(report_name + '.pdf'))
    # ]
    #
    # return request.make_response(pdf_content, headers=pdfhttpheaders)



    #

