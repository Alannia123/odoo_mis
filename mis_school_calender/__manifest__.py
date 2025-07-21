# -*- coding: utf-8 -*-

{
    'name': 'Educational School calender MIS',
    'version': '17.0.1.0.1',
    'category': 'Extra Tools',
    'summary': """Calender for Education erp""",
    'description': """Education Time Table provides a comprehensive timetable 
     management system, enhancing the functionality of  educational 
     institutions.""",
    'author': 'Alanniainfotechz',
    'company': 'Alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['mis_education_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/calender_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
