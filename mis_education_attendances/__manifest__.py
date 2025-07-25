# -*- coding: utf-8 -*-

{
    'name': 'Educational Attendance Management MIS',
    'version': '17.0.1.0.0',
    'category': 'School',
    'summary': """"Openerp to Student Attendance Management System for 
     Educational ERP""",
    'description': """An easy and efficient management tool to manage and 
     track student attendance. Enables different types of filtration to 
     generate the adequate reports""",
    'author': 'Alanniainfotechz',
    'company': 'Alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['mis_education_core'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'report/monthly_attendance_report_view.xml',
        'reports/report_monthly_attendance.xml',
        # 'reports/division_attendance_report.xml',
        'views/education_attendance_line_views.xml',
        'views/education_attendance_views.xml',
        'views/education_class_division_views.xml',
        'views/education_student_views.xml',
        'wizard/monthly_attendance_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/mis_education_attendances/static/src/css/attendance.css'
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
