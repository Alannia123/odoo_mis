# -*- coding: utf-8 -*-

{
    'name': ' MIS School Education Management Website Management',
    'version': '17.0',
    'category': 'School',
    'summary': """Manage the MIS School Website education system""",
    'description': """This modules helps to organize the website data and helps to update the website datas""",
    'author': 'Alannia',
    'company': 'alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['base','mis_education_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'views/program_gallery_view.xml',
        'views/events_aws_view.xml',
        'views/web_info_view.xml',
        'views/web_video_view.xml',
        'views/magazine_view.xml',
        'views/members_view.xml',
        'views/web_slide_view.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',
    ],
     'assets': {
        'web.assets_backend': [
            'mis_website_backend/static/src/js/document_multi_upload.js',
            'mis_website_backend/static/src/xml/document_multi_upload.xml',
            'mis_website_backend/static/src/js/slide_images.js',
            'mis_website_backend/static/src/xml/slide_image_view.xml',
        ],
    },

    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
