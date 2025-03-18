# -*- coding: utf-8 -*-

{
    'name': ' MIS School Education Management Hoe Work Anouncements',
    'version': '17.0',
    'category': 'School',
    'summary': """Manage the MIS School Website education system""",
    'description': """This modules helps to organize the website data and helps to update the website datas""",
    'author': 'Alannia',
    'company': 'alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['base','mis_education_core', 'mis_website_backend'],
    'data': [
        'security/ir.model.access.csv',
        # 'data/sequence.xml',
        # 'data/homework_cron.xml',
        'wizard/home_entry_wizard_view.xml',
        'views/home_work_view.xml',
        # 'views/student_view.xml',
        'views/anounce_view.xml',
    ],
    #  'assets': {
    #     'web.assets_backend': [
    #         # 'mis_website_backend/static/src/js/multi_upload.js',
    #         'mis_website_backend/static/src/js/document_multi_upload.js',
    #         'mis_website_backend/static/src/xml/document_multi_upload.xml'],
    # },

    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
