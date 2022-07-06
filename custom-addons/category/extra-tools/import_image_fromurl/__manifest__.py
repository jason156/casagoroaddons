{
    'name': 'Import Images From URL / CSV / XLS',
    'version': '1.2',
    'category': 'Tools',
    'author': 'FreelancerApps',
    'depends': ['base', 'sale', 'product'],
    'summary': 'Import Product, Customer, Supplier Images From URL, csv, xls file Import Image URL CSV XLS Import Image URL CSV Import Image V Image XLS Import URL Image URL Image CSV  Import Image URL Image CSV URL Import',
    'description': '''
Import Product, Customer, Supplier Images From Direct URL / CSV / XLS File
==========================================================================
Add image url directly into Product, Customer, Supplier and system will be automatically import or download image from that url and set to that object
Add Image URL into csv / xls file and import that file then system will be automatically import or download image from that url and set to that object

Key features:
-------------
* Easy To Use.
* Import images from url for product, customer, supplier.
* Import Via directly adding url, csv file, xls file.
* For csv / xls file you have an option to select mapping field like database id, name, internal reference.
* Supporting Create and Write option. So if you update URL and Edit and Save it read again and set Image.
* Maintains Log, so user can check when file was imported and check error if any.
* Set access right, so specific user will set image though url/csv/xls file.

<Search Keyword for internal user only>
---------------------------------------
Import Image URL CSV XLS Import Image URL CSV Import Image URL XLS Import Image CSV URL Import Image CSV  Import Image URL Image CSV URL Import 
    ''',
    'data': [
        'security/import_image_security.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/res_partner_view.xml',
        'wizard/upload_url_file_view.xml',
    ],
    'images': ['static/description/import_from_url_banner.png'],
    'price':9.99,
    'currency': 'USD',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
