
{
    'name': 'Odoo Mini Tickets',
    'summary': """Detalle de la Venta en el Ticket""",
    'version': '1.0',
    'description': """Impresón Mini Tickets""",
    'author': 'ITSS',
    'company': 'German PoncDominguez',
    'author': 'German Ponce Dominguez',
    'website': 'http://poncesoft.blogspot.com',
    "support": "german.poncce@outlook.com",
    'category': 'Point of Sale',
    'version': '13.0.0.1.0',
    'depends': ['base', 'point_of_sale', 'pos_restaurant'],
    'license': 'LGPL-3',
    'data': [         
        'views/views.xml',
        'views/templates.xml',
        ],
    'qweb': [
             'static/src/xml/pos_ticket_view.xml',
             #'static/src/xml/assets_extend.xml',
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
