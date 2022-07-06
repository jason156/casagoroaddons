# -*- coding: utf-8 -*-
{
    'name': "Responsive for pos screen",

    'summary': """
        Mobile view for pos screen.
    """,

    'description': """
        Responsive for pos screen.
    """,
    'price': 45,
    'currency': 'EUR',
    'author': "Srikesh Infotech",
    'license': "AGPL-3",
    'website': "www.srikeshinfotech.com",
    'category': 'point_of_sale',
    'version': '13.0.0.2',
    'images': ['images/main_screenshot.png'],
    'depends': ['point_of_sale'],
    'qweb': ['static/src/xml/pos.xml',
     ],
    'data': [
        'views/pos_responsive.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
