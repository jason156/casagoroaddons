# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name' : "Similiar Products Suggestion",
    'version' : "13.0.0.0",
    'author' : "BrowseInfo",
    'description' : '''
            This module adds a feature in product to have suggested products.
			send suggested product by email to customer, product suggestion, item suggestion, website product suggestion, email suggested item. Product send by email. Suggested product send by email, suggested product for customer, Similiar product suggestion for customer, Similiar product suggestion for partner.
    ''',
    
    'summary': 'Similar Products Suggestion to the customer by email.',
    'category' : "Website",
    'data': [
             'edi/mail_template_data.xml',
             'views/product_view.xml',
             ],
    'website': 'http://www.browseinfo.com',
    'depends' : ['sale_management','stock'],
    'installable': True,
    'auto_install': False,
	"images":['static/description/Banner.png'],

}
