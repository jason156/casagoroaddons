from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools import ustr

sitesearchapp_api = {'test_api': 'api/check', 'indices_api': 'api/indices', 'index_api': 'api/index',
                     'delete_api': 'api/delete', 'search_api': 'api/search', 'documents_api': 'api/index-ids',
                     'log_api': 'api/querylog'}


class SiteSearchAppConfig(models.Model):
    _name = 'searchapp.search.config'
    _inherit = 'res.config.settings'

    enable = fields.Boolean('Enable', default=True)
    host = fields.Char('Host')
    user = fields.Char('User')
    api_key = fields.Char('API Key')
    password = fields.Char('Password')
    alignment = fields.Selection([('left', 'Left'), ('center', 'Center'), ('right', 'Right')],
                                 'Search Suggestions Box Alignment', default='right')
    ip_whitelist = fields.Char('Whitelist IP',
                               help="Comma-separated list of IP Addresses excluded from search logging.")
    text_color = fields.Char('Text Color')
    title_color = fields.Char('Title Color')
    price_color = fields.Char('Price Color')
    border_color = fields.Char('Border Color')
    loader_color = fields.Char('Loader Color')
    slash_color = fields.Char('Price Slash Color')
    highlight_color = fields.Char('Highlight Color')
    hover_color = fields.Char('Hover Background Color')
    bg_color = fields.Char('Container Background Color')
    title_bg_color = fields.Char('Title Background Color')
    custom_css = fields.Text('Custom CSS', help="Create custom css styles. Paste your code here.")

    def set_values(self):
        super(SiteSearchAppConfig, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('searchapp.search.config', 'host', self.host or '')
        IrDefault.set('searchapp.search.config', 'user', self.user or '')
        IrDefault.set('searchapp.search.config', 'enable', self.enable or '')
        IrDefault.set('searchapp.search.config', 'api_key', self.api_key or '')
        IrDefault.set('searchapp.search.config', 'password', self.password or '')
        IrDefault.set('searchapp.search.config', 'ip_whitelist', self.ip_whitelist or '')
        IrDefault.set('searchapp.search.config', 'alignment', self.alignment)
        IrDefault.set('searchapp.search.config', 'text_color', self.text_color or '#333333')
        IrDefault.set('searchapp.search.config', 'hover_color', self.hover_color or '#EEEEEE')
        IrDefault.set('searchapp.search.config', 'title_color', self.title_color or '#333333')
        IrDefault.set('searchapp.search.config', 'price_color', self.price_color or '#333333')
        IrDefault.set('searchapp.search.config', 'loader_color', self.loader_color or '#B6BD34')
        IrDefault.set('searchapp.search.config', 'border_color', self.border_color or 'transparent')
        IrDefault.set('searchapp.search.config', 'title_bg_color', self.title_bg_color or '#CECECE')
        IrDefault.set('searchapp.search.config', 'bg_color', self.bg_color or '#FFFFFF')
        IrDefault.set('searchapp.search.config', 'slash_color', self.slash_color or '#333333')
        IrDefault.set('searchapp.search.config', 'highlight_color', self.highlight_color or '#000000')
        IrDefault.set('searchapp.search.config', 'custom_css', self.custom_css or '')

    @api.model
    def get_defaults(self):
        IrDefault = self.env['ir.default'].sudo()
        return IrDefault.get_model_defaults('searchapp.search.config')

    @api.model
    def get_default(self, ssa_api):
        IrDefault = self.env['ir.default'].sudo()
        host = IrDefault.get('searchapp.search.config', 'host')
        endpoint = sitesearchapp_api.get(ssa_api)
        res = ''
        if host and endpoint:
            if host.endswith('/'):
                res = '%s%s' % (host, endpoint)
            else:
                res = '%s/%s' % (host, endpoint)
        else:
            res = ''
        return res

    def get_indices(self):
        searchapp_model = self.env['searchapp.search']
        try:
            searchapp_model.get_indices()
        except Exception as e:
            raise UserError("%s" % ustr(e))
        return {
            'name': 'SiteSearchApp Indexer',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'searchapp.search',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def index_site(self):
        searchapp_model = self.env['searchapp.search']
        try:
            searchapp_model.index_site()
        except Exception as e:
            raise UserError("%s" % ustr(e))
        raise UserError("Successfully indexed site to SiteSearchApp!")

    def test_connection(self):
        self.ensure_one()
        host = self.get_default('test_api')
        searchapp_model = self.env['searchapp.search']
        try:
            res = searchapp_model.get_api_response(host=host)
            if res and res.get('error'):
                raise UserError("%s" % res['error'])
            if res and not res.get('status'):
                raise UserError("%s" % res['message'])
        except UserError as e:
            raise UserError("%s " % ustr(e))

        raise UserError("SiteSearchApp Connection Test Succeeded!")
