# Copyright 2020  HSP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "tree edit and mass editing by HSP",

    'summary': """tree edit and mass edit 
    tree视图可编辑和多记录编辑
    """,
   'license': 'LGPL-3',
   'description': """
    tree edit and mass edit 
    tree视图可编辑和多记录编辑
   """,
    'author': 'HSP',
    'website': "https://www.garage-kit.com",
    'images': ['static/description/logo.png'],
    'category': 'Tools',
    'version': '13.0.1.0.0',
  
    'depends': [
        'base', 'web',
    ],
    'data': [
        'views/template.xml'
    ],
    # 'demo': [
    #     'demo/report.xml',
    # ],
    'installable': True,
}
