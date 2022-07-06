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
    'name': 'Modulo Base para los Web Services de AFIP',
    'version': '13.0.1.0.0',
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'PRONEXO.COM ADHOC, Moldeo,Odoo Community Association (OCA)',
    'website': 'https://www.pronexo.com',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'l10n_ar',  # needed for CUIT and also demo data
        # TODO this module should be merged with l10n_ar_afipws_fe as the dependencies are the same
    ],
    'external_dependencies': {
        'python': ['pyafipws', 'OpenSSL', 'pysimplesoap']
    },
    'data': [
        'wizard/upload_certificate_view.xml',
        'views/afipws_menuitem.xml',
        'views/afipws_certificate_view.xml',
        'views/afipws_certificate_alias_view.xml',
        'views/afipws_connection_view.xml',
        'views/res_config_settings.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/ir.actions.url_data.xml',
    ],
    'demo': [
        'demo/certificate_demo.xml',
        'demo/parameter_demo.xml',
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
