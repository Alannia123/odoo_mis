# -*- coding: utf-8 -*-

{
    'name': 'Educational ERP Dashboard MIS',
    'version': '17.0.1.0.0',
    'category': 'Industries, Productivity',
    'summary': 'An integrated view of the education ERP system',
    'description': """A comprehensive module designed to provide educational 
                    institutions to manage and monitor various operations""",
    'author': "Alanniainfotechz",
    'company': 'Alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['base', 'mis_education_attendances', 'mis_education_promotion',
                'mis_education_time_table'],
    'data': [
        'security/education_security.xml',
        'security/ir.model.access.csv',
        'views/erp_dashboard_views.xml'],
    'assets': {
        'web.assets_backend': [
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&amp;display=swap',
            'mis_education_erp_dashboard/static/src/css/dashboard.css',
            'mis_education_erp_dashboard/static/src/js/dashboard.js',
            'mis_education_erp_dashboard/static/src/xml/erp_dashboard_templates.xml',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
