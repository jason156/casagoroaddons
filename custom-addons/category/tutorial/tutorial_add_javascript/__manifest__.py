# -*- coding: utf-8 -*-
{
    'name': "Tutorial adding assets",

    'summary': """
        Tutorial about how to create and use Javascript files in Odoo""",

    'description': """
        This module is a tutorial in the form of an app. In this app you can find the code to create and use
        JavaScript functionalities in Odoo 13.
    """,

    'author': "Oocademy",
    'website': "http://www.oocademy.com",
    'price': 0.00,
    'currency': 'EUR',
    'category': 'Tutorial',
    'version': '13.0.0.1',
    'license': 'Other proprietary',
    'depends': ['base','web'],
    'images': [
        'static/description/banner.jpg',
    ],

    'data': [
        'views/assets.xml',
    ],
    'application': True,
}
