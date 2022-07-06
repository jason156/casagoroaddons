# -*- coding: utf-8 -*-
{
    'name': 'Rearrange Product Variants / Variant Mapping',
    'version': '11.0.1.0',
    'license': 'Other proprietary',
    'category': 'Sales',
    'summary': """This app allows user to remap product variants. User can rearrange varinats and change 
                    the template of variant with easy drag and drop interface.
                    Keywords
                    Remap Variant Change Template change variant recreate move variant 
                    new variant variants templates change parent Re-arrange variants Re-arrange templates
                    Assign Template Dashboard product management interface product view variant manager
                    Re-map variant Re-map Tempaltes
                """,
    'author':'Craftsync Technologies',
    'maintainer': 'Craftsync Technologies',
    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'sequence': 1,
    'depends': [
        'product'
    ],
    
    'data': [
        'views/product_views.xml',
        'report/variant_mapping_templates.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'price': 29.00,
    'currency': 'EUR',
 }

