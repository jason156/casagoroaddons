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
    'name': 'Argentinian Accounting UX',
    'version': "13.0.1.0.0",
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'PRONEXO.COM ADHOC',
    'website': 'https://www.pronexo.com',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'l10n_ar',
        'account_check',
        # for payment group report
        'account_withholding',
        'account_payment_group_document',
    ],
    'data': [
        'data/res_currency_data.xml',
        'data/account_account_tag_data.xml',
        'data/account_tax_group_data.xml',
        'data/account_chart_template_data.xml',
        'data/account_tax_template_data.xml',
        'views/portal_templates.xml',
        'views/account_move_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/afip_concept_view.xml',
        'views/afip_activity_view.xml',
        'views/afip_tax_view.xml',
        'views/res_config_settings_views.xml',
        'reports/report_payment_group.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
