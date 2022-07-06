# -*- coding: utf-8 -*-
{
    'name': "quant distribute",
    'summary': """
        Divide el quant entre diferentes ubicaciones""",

    'description': """
        Divide el quant entre diferentes ubicaciones
    """,

    'author': "Filoquin",
    'website': "http://www.sipecu.com.ar",
    'category': 'Casa Goro',
    'version': '13.0.0.1',
    'depends': ['stock', 'stock_distribute', 'web_widget_x2many_2d_matrix'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_quant_distribute.xml',
    ],
}
