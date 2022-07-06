# -*- coding: utf-8 -*-
{
    'name': "merge products",

    'summary': """Unificar variantes en una plantilla""",

    'description': """
        Unificar variantes en una plantilla
    """,

    'author': "filoquin",
    'website': "http://www.sipecu.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'product',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['product'],
    'external_dependencies': {
        'python': ['PyYAML']
    },

    'data': [
        'views/product_merge.xml',
    ],
}
