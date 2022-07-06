# -*- coding: utf-8 -*-
{
    'name': "Goro price wizard",

    'summary': """
        Wizard para establecer precios""",

    'description': """
        Wizard para establecer precios
    """,

    'author': "Filoquin",
    'website': "http://www.sipecu.com.ar",
    'category': 'Casa Goro',
    'version': '0.2',
    'depends': ['product', 'product_replenishment_cost'],
    'auto_install': False,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_price_wiz.xml',
        'views/product_pricelist.xml',
        'views/res_currency.xml',
        'views/product_multi_price_wiz.xml'
    ],
}
