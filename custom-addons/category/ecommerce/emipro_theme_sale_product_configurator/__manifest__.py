{
    #Module information
    'name': 'Emipro Theme Sale Product Configurator',
    'category': 'eCommerce',
    'summary': 'This app contains inherits the sale product configuration design templates.',
    'version': '1.0.0',
    'license': 'OPL-1',
    'depends':['sale_product_configurator'],

    'data': [
        'templates/assets.xml',
        'templates/cart.xml',
    ],

    #Odoo Store Specific
    'images': [
	    'static/description/Emipro-Theme-sale-configurator.jpg',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical
    'installable': True,
    'auto_install': False,
    'price': 0.00,
    'currency': 'EUR',
}
