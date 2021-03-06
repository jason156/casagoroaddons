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
    'name': 'Purchase Suggest',
    'version': '13.0.1.0.0',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'summary': 'Suggest POs from special suggest orderpoints',
    'author': 'PRONEXO.COM, Akretion',
    'website': 'http://www.pronexo.com',
    'depends': [
        'purchase_stock_ux',
        # 'purchase_suggest',
        'product_replenishment_cost',
    ],
    'conflicts': ['procurement_suggest'],
    'data': [
        'views/stock_view.xml',
        'wizard/purchase_suggest_view.xml',
    ],
    'installable': True,
}
