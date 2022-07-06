from odoo import models, api


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):

        res = super()._name_search(name, args, operator, limit, name_get_uid)
        if not res:
            res = []
        if not args: 
            args = []
        if not limit:   
            limit = 100
        if name and len(res) < limit:
            limit = limit - len(res)
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            product_ids = []
            if operator in positive_operators:
                product_ids = self._search(
                    [('modelo_articulo', operator, name)] + args, limit=limit, access_rights_uid=name_get_uid)

                res += models.lazy_name_get(self.browse(
                    product_ids).with_user(name_get_uid))

        return res


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if len(self.categ_id.public_categ_id):

            self.public_categ_ids = [
                (6, 0, [self.categ_id.public_categ_id.id])]

    """@api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):

        res = super()._name_search(name, args, operator, limit, name_get_uid)

        return res"""
