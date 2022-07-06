# -*- coding: utf-8 -*-
# Copyright 2019 OdooERPCloud.
#    @author Juan Carlos Montoya <jcmontoya@odooerpcloud.com>
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Backend Theme V12 Styles",
    "summary": "Backend Theme V12 Styles",
    "version": "0.1",
    "category": "Theme/Backend",
    "website": "https://www.odooerpcloud.com",
    "description": """
		Backend theme for Odoo Override Styles
    """,
    "author": "Openworx, OdooERPCloud",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'web',
        'backend_theme_v12',

    ],
    "data": [
        'views/assets.xml',
    ],
    'live_test_url': 'https://youtu.be/JX-ntw2ORl8'
}
