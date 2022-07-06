# -*- coding: utf-8 -*-
{
    'name': "Systray Translate",
    'summary': """Integrated Translator within the odoo framework""",
    'description': """Helps to translate words and phrases between English and over 100 other languages.""",
    'version': '13.0.1.0.0',
    'category': 'Tools',
    'author': "Kripal K",
    'website': "https://www.linkedin.com/in/kripal754/",
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'external_dependencies': {
        'python': ['googletrans'],
    },
    'qweb': ['static/src/xml/systray_translator.xml'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
