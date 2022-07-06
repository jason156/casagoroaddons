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
    'name': 'Sale Three Discounts UX',
    'version': '13.0.1.0.0',
    'category': 'Sales Management',
    'sequence': 14,
    'author': 'PRONEXO.COM ADHOC',
    'website': 'https://www.pronexo.com',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'sale_ux',
        'sale_three_discounts',
    ],
    'data': [
        'wizards/sale_order_global_discount_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}
