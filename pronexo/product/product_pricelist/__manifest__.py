##############################################################################
#
#    Copyright (C) 2019  pronexo.com  (https://www.pronexo.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Pricelists information on Products",
    'version': '12.0.1.0.0',
    'category': 'Sales & Purchases',
    'sequence': 14,
    'author': 'PRONEXO.COM ADHOC',
    'website': 'https://www.pronexo.com',
    'license': 'AGPL-3',
    "depends": [
        'sale',
    ],
    "data": [
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/product_pricelist_views.xml',
        # set pricelist groups
        'security/product_pricelist_security.xml',
        # set default formula on sale settings configuration
        'data/product_pricelist_data.xml',
    ],
    'demo': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
