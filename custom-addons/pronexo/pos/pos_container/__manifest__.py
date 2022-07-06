# -*- coding: utf-8 -*-
{
    'name': 'PoS Container',
    'version': '11.0.1.0.0',
    'author': 'HomebrewSoft',
    'website': 'https://gitlab.com/HomebrewSoft/heladeria/pos_container',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        # security
        # data
        # reports
        # views
        'templates/pos.xml',
        'views/product_template.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
}
