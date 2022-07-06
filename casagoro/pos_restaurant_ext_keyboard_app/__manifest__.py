# -*- coding: utf-8 -*-
{
    "name": "Point of Sale & Restaurant Keyboard Shortcut",
    "author": "Edge Technologies",
    "version": "13.0.1.0",
    "live_test_url": 'https://youtu.be/P-AcmYxWrrg',
    "images": ["static/description/main_screenshot.png"],
    'summary': 'POS keyboard shortcuts enable keyboard shortcut in pos Shortcut Access keyboard Shortcut in Point Of Sale keyboard in POS User wise set keyboard shortcuts for POS Keyboard Shortcuts for Point Of Sale POS shortcut keys Shortcuts keys on pos easy keyboard',
    "description": """
    
   This app help to enable keyboard shortcuts for both restaurant and normal POS
POS Keyboard Shortcuts Pos Shortcut Access keyboard Shortcut accessible in Point Of Sale keyboard in POS keyboard shortcuts User wise set keyboard shortcuts Keyboard Shortcuts for POS Keyboard Shortcuts for Point Of Sale Pos Shortcut Access point of sale with keyboard shortcuts POS shortcut keys Shortcuts keys odoo Keyboard shortcut Keyboard shurtcut Odoo
odoo pos keyboard shortcuts , odoo pos shortcut keys pos shortcut keys 
    
    """,
    "license": "OPL-1",
    "depends": ['base', 'sale_management', 'point_of_sale', 'pos_restaurant'],
    "data": [
        'views/pos_js.xml',
        'views/pos_payment.xml',
    ],
    'qweb': [
        'static/src/xml/pos_key.xml',
    ],
    "auto_install": False,
    "installable": True,
    "price": 18,
    "currency": 'EUR',
    "category": "Point of Sale",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
