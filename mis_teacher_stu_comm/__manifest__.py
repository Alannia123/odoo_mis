# -*- coding: utf-8 -*-

{
    'name': ' MIS School Education Teachers To Student Management ',
    'version': '17.0',
    'category': 'School',
    'summary': """MIS School Education Teachers To Student Management system""",
    'description': """This modules helps to organize the website data and helps to update the website datas""",
    'author': 'Alannia',
    'company': 'alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['base','hr', 'mis_education_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/teacher_class_view.xml',
        'views/teacher_parent_view.xml',
    ],


    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
