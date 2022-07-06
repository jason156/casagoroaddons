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
    'name': 'Sale Report Last Sale',
    'summary': 'Adds a report view to show how many days '
               'have passed since a partner ordered a product',
    'version': '13.0.1.0.0',
    'depends': [
        'sale',
    ],
    'author': 'Ivan Todorovich,'
              'Odoo Community Association (OCA),'
              'PRONEXO.COM ADHOC',
    'license': 'AGPL-3',
    'data': [
        'reports/sale_last_sale_report.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'category': 'Sale',
    'installable': True,
}