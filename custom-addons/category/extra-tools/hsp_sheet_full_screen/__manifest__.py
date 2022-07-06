# Copyright 2019 EINFO HSP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "odoo enterprise sheet full screen by HSP",

    'summary': """
    odoo enterprise sheet full screen
    odoo企业版表单全屏显示
   """,
   'license': 'LGPL-3',
   'description': """
    odoo enterprise sheet full screen
    odoo企业版表单全屏显示
   """,
    'author': 'HSP',
    'website': "https://www.garage-kit.com",
    'images': ['static/description/2.gif'],
    'category': 'Tools',
    'version': '13.0.1.0.0',
  
    'depends': [
        'web_enterprise',
    ],
    'data': [
        'views/webclient_templates.xml',
    ],
    # 'demo': [
    #     'demo/report.xml',
    # ],
    'installable': True,
}
