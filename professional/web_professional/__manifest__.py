# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Professional',
    'category': 'Hidden',
    'version': '1.0',
    'description':
        """
Odoo Professional Web Client.
===========================

This module modifies the web addon to provide Professional design and responsiveness.
        """,
    'depends': ['web'],
    'auto_install': True,
    'data': [
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'license': 'OEEL-1',
}
