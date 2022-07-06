# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Order Queue',
    'version': '13.0.1.0.0',
    'category': 'Point of Sale',
    'author': 'Anggara.id',
    'sequence': 5,
    'summary': """Speed Up the Pos Order at Odoo Point of sale using the queue method.""",
    'license': 'LGPL-3',
    'description': """ 
        POS Order Queue v13.0
        Speed Up the Pos Order at Odoo Point of sale using the queue method. """,
    'depends': [
        'base','point_of_sale'
    ],
    'support': 'halo@anggara.id',
    'data': [
        'data/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/posorder_tmp_view.xml',
        # 'views/pos_session_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'website': "https://anggara.id/",
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 30.99,
    'currency': 'USD'
}
