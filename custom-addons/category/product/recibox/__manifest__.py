# -*- coding: utf-8 -*-
{
    'name': "Recibo X",

    'summary': """
Permite imprimir recibo X""",

    'description': """
        invoice.l10n_latam_document_type_id 
    """,

    'author': "Girolami Juan",
    'website': "http://www.casagoro.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_latam_invoice_document'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],

}
