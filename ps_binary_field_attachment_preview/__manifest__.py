{
    'name': 'Binary Field Attachment Preview',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Preview attachments for binary fields',
    'description': """
        This module adds a preview functionality for all binary fields
        using the 'binary' widget in Odoo 17.
    """,
    'author': 'Pysquad Informatics LLP',
    'website': 'https://www.pysquad.com',
    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',
    ],

    'assets': {
        'web.assets_backend': [
            'ps_binary_field_attachment_preview/static/src/js/binary_field_preview.js',
            'ps_binary_field_attachment_preview/static/src/xml/binary_field_preview.xml',
        ],
    },

    # Images
    'images': [
        'static/description/banner_img.png',
    ],


    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
