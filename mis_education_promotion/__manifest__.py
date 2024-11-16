# -*- coding: utf-8 -*-

{
    'name': 'Educational Promotion MIS',
    'version': '17.0.1.0.0',
    'category': 'Industries',
    'summary': 'Promotion of students after each Academic year',
    'description': """ This module providing the facility of academic 
     transitions,enabling the promotion of students to respective higher 
     classes without hassle. """,
    'author': 'Alanniainfotechz',
    'company': 'Alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['mis_education_exam'],
    'data': [
        'security/ir.model.access.csv',
        'views/education_promotion_views.xml',
        'views/education_student_final_result_views.xml',
        'views/education_student_views.xml',
        'views/education_class_division_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
