# -*- coding: utf-8 -*-

{
    'name': ' MIS School Education Teachers Task Management ',
    'version': '17.0',
    'category': 'School',
    'summary': """Manage the MIS School Website education system""",
    'description': """This modules helps to organize the website data and helps to update the website datas""",
    'author': 'Alannia',
    'company': 'alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['base','hr', 'mail', 'mis_education_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/activity.xml',
        'data/sequence.xml',
        'views/task_mgnt_view.xml',
    ],


    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
