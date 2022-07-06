# -*- coding: utf-8 -*-
{
    'name': 'POS Test/Sample Orders',
    'version': '13.0.1.0',
    'summary' : 'Create sample,dummy or test pos order. No any information related to order stored in database.',
    'category': 'Point Of Sale',
    'depends': ['point_of_sale'],
    'description': '''
User can create test, sample or dummy orders in Odoo. 
If user create test order, than that order entry is not created in odoo, so its not shown to anyone.
Its useful, when user generally want to avoid pay more taxes.
Hide order, Sample order, dummy order, sample pos order, dummy pos order, hide pos order,pos test order, pos dummy order, pos sample order,
pos test mode, pos test toggle mode, fake order,cheat order, dashboard, pos report, import, export, pdf export, excel export
    ''',
    'author': "Nilesh Sheliya",
    'website': 'http://sheliyainfotech.com',
    'data': [
             'views/pos_templates.xml'
        ],
    'qweb': ['static/src/xml/pos.xml'],
    "images": ["static/description/image/banner.png"],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
