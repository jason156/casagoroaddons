# -*- coding: utf-8 -*-
{
    'name': "Server Action",

    'summary': """
         Start, Stop and Restart odoo server through odoo interface""",

    'description': """
Functionalities
===============
-> Manage server details with its url,username,password and commands
-> Start, Stop and Restart odoo server through odoo interface
-> Maintain history to manage who perform the server action and when
    """,
    'author': "Aktiv software ",
    'website': "http://www.aktivsoftware.com/",
    'category': 'Extra Tools',
    'version': '13.0.1.0.0',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'security/server_action_security.xml',
        'security/ir.model.access.csv',
        'views/server_action_views.xml',
        'views/warning_box.xml',
    ],
    'demo': ['demo/demo.xml'],
    'images': ['static/description/banner.jpg'],
}
