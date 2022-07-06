# -*- coding: utf-8 -*-
{
    'name': 'Mail Messages Draft.'
            ' Save Message as Draft, Edit Message Drafts, Send Message from Draft Message',
    'version': '13.0.1.0.0',
    'summary': """Adds draft messages support to free 'Mail Messages Easy' app""",
    'author': 'Ivan Sokolov, Cetmix',
    'category': 'Discuss',
    'license': 'LGPL-3',
    'website': 'https://cetmix.com',
    'live_test_url': 'https://demo.cetmix.com',
    'description': """
Mail Messages Drafts
""",
    'depends': ['prt_mail_messages'],
    'images': ['static/description/banner.png'],

    'data': [
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/prt_mail_draft.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
