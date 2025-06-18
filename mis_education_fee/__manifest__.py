# -*- coding: utf-8 -*-

{
    "name": "Educational Fee Management MIS",
    "version": '17.0.1.0.1',
    "category": 'Industries',
    'summary': """Education fee is the core module of Educational ERP software, 
     a management application for effective school run .""",
    'description': """Education fee provides a comprehensive student fee
     management solution to automate, streamline and transform fee processing
     in educational institutions.""",
    "author": "Alanniainfotechz",
    "company": "Alanniainfotechz",
    'maintainer': 'Alanniainfotechz',
    "depends": ['account', 'mis_education_core'],
    "data": [
        'security/ir.model.access.csv',
        'views/education_fee_structure_menu_views.xml',
        'views/account_move_line_views.xml',
        'views/education_fee_structure_views.xml',
        'views/education_fee_type_views.xml',
        'views/education_fee_category_views.xml',
        'views/account_journal_templates.xml',
        'views/account_journal_views.xml',
    ],
    "demo": [
        "demo/account_account_demo.xml",
        'demo/account_journal_demo.xml',
        "demo/education_fee_category_demo.xml",
        'demo/education_fee_structure_demo.xml',
        'demo/education_fee_type_demo.xml',
        'demo/education_fee_structure_lines_demo.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    "installable": True,
    "auto_install": False,
    'application': True,
}
