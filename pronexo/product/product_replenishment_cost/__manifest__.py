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
    'name': 'Replenishment Cost',
    'version': '13.0.1.1.0',
    'author': "PRONEXO.COM ADHOC, Camptocamp,GRAP,Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'category': 'Products',
    'depends': [
        # for use the user company currency for the standard price
        'product_ux',
        # for page in product form
        'purchase',
        # for access rights
        'sales_team',
        # only for menu for cost rules
        'sale',
    ],
    'website': 'https://www.pronexo.com/',
    'data': [
        'security/product_replenishment_cost_security.xml',
        'data/ir_cron_data.xml',
        'views/product_template_views.xml',
        'views/product_replenishment_cost_rule_views.xml',
        'views/product_supplierinfo_views.xml',
        'wizards/product_update_from_replenishment_cost_wizard_views.xml',
        'demo/product_replanishment_cost_demo.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
