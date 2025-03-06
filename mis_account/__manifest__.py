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
    'depends': ['base','account'],
    'data': [
        'views/account_move_view.xml',
        'views/report_invoice.xml',
        'views/invoice_report_template.xml',
        'views/invoice_ir_actions.xml',
    ],

    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
