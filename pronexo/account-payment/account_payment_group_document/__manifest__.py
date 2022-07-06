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
    "name": "Payment Groups with Accounting Documents",
    "version": "13.0.1.0.0",
    "author": "PRONEXO.COM,Odoo Community Association (OCA)",
    "website": "https://www.pronexo.com",
    "license": "AGPL-3",
    "category": "Accounting",
    "depends": [
        "l10n_latam_invoice_document",
        "account_payment_group",
    ],
    "data": [
        'view/account_payment_group_view.xml',
        'view/account_payment_receiptbook_view.xml',
        'wizards/account_payment_group_invoice_wizard_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/decimal_precision_data.xml',
        'data/l10n_latam.document.type.csv',
    ],
    "demo": [
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': True,
}
