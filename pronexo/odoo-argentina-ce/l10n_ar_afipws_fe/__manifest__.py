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
    "name": "Factura Electrónica Argentina",
    'version': '13.0.1.0.0',
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'PRONEXO.COM ADHOC, Moldeo, Odoo Community Association (OCA)',
    'website': 'https://www.pronexo.com',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'l10n_ar_afipws',
        'l10n_ar',
        'account_debit_note',
    ],
    'external_dependencies': {
    },
    'data': [
        'views/account_move_views.xml',
        'views/account_journal_view.xml',
        'views/report_invoice.xml',
        'views/menuitem.xml',
    ],
    'demo': [
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
