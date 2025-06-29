# -*- coding: utf-8 -*-

{
    'name': ' MIS School Student Portal',
    'version': '17.0',
    'category': 'School',
    'summary': """Manage the MIS School Website Student Portal""",
    'description': """This modules helps to organize the website Student Portal""",
    'author': 'Alannia',
    'company': 'alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['web','website','portal', 'account', 'mis_website', 'mis_education_erp_dashboard', 'mis_homework'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/web_menu.xml',
        'views/student_account_template.xml',
        'views/announce_template.xml',
        'views/home_work_template.xml',
        'views/student_info_temp.xml',
        'views/time_table_template.xml',
        'views/class_comm.xml',
        'views/attendance_template.xml',
        'views/teacher_stu_view.xml',

    ],

    # 'assets': {
    #     'web.assets_backend': [
    #         '/mis_website/static/src/js/video_field.xml'
    #         '/mis_website/static/src/js/video_field.js'
    #     ],
    # },
    'assets': {
        'web.assets_frontend': [
            # '/mis_student_portal/static/src/css/dashboard.css',
            # '/mis_website/static/src/css/sample.css',
        ],
    },


    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
