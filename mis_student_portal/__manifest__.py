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
    'depends': ['web','website','portal', 'mis_website'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/web_menu.xml',
        'views/student_account_template.xml',
        # 'views/home_template.xml',
        # 'views/prospectus_template.xml',
        # 'views/academics_template.xml',
        # 'views/school_commitee_temp.xml',
        # 'views/program_and_events.xml',
        # 'views/online_application_templates.xml',
        # 'views/student_portal_templates.xml',
        # # 'views/nav_bar_template.xml',
        # 'views/website_header.xml',
        # 'views/login_logo.xml',

    ],

    # 'assets': {
    #     'web.assets_backend': [
    #         '/mis_website/static/src/js/video_field.xml'
    #         '/mis_website/static/src/js/video_field.js'
    #     ],
    # },
    'assets': {
        'web.assets_frontend': [
            '/mis_website/static/src/css/style.css',
            # '/mis_website/static/src/css/sample.css',
            '/mis_website/static/src/js/online_application.js',
            '/mis_website/static/src/js/valaidate_js.js',
        ],
    },


    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
