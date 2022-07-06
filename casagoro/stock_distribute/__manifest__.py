# -*- coding: utf-8 -*-
{
    'name': "stock distribute",
    'summary': """
        Divide el stock entre diferentes ubicaciones""",

    'description': """
        Divide el stock entre diferentes ubicaciones
    """,

    'author': "Filoquin",
    'website': "http://www.sipecu.com.ar",
    'category': 'Casa Goro',
    'version': '13.0.1.0',
    'depends': ['stock', 'web_widget_x2many_2d_matrix'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_location.xml',
        'views/stock_distribute.xml',
        'views/stock_picking.xml',
        'views/stock_warehouse.xml'
    ],
}
