# -*- coding: utf-8 -*-
{
    'name': "goro_ux",
    'summary': """
        Correciones a la UX para casa goro""",

    'description': """
        Correciones a la UX para casa goro
    """,
    'author': "filoquin",
    'website': "http://www.sipecu.com.ar",
    'category': 'UX',
    'version': '13.0.0.1',

    'depends': ['product', 'point_of_sale', 'website', 'product_pricelist_direct_print'],

    'data': [
        'data/res_groups.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/pos_payment.xml',
        'views/etiqueta_expreso.xml',
        'views/product_pricelist_image.xml',
        'views/purchase_order.xml',
        'views/stock.xml'
    ],
}
