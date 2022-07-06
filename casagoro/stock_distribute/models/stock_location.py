from odoo import fields, models


class StockLocation(models.Model):

    _inherit = 'stock.location'

    distribute = fields.Boolean(
        string='Distribute',
    )

    distribute_part = fields.Float(
        string='Distribute part',
    )
    distribute_sequence = fields.Integer(
        string='sequence',
        default=10
    )

    def name_get(self):
        if 'from_stock_distribute' in self._context:

            res = []
            for rec in self:
                name = '%s' % rec.name
                res.append((rec.id, name))
            return res
        return super().name_get()


class StockMove(models.Model):

    _inherit = 'stock.move'

    distributed = fields.Boolean(
        string='distributed',
    )
    distributed_qty = fields.Float(
        string='distributed qty',
        copy=False
    )

    def name_get(self):

        if 'from_stock_distribute' in self._context:

            res = []
            for rec in self:
                name = '%s %s %s %s %s' % (
                    rec.product_id.default_code or '', rec.product_id.barcode or '',
                    rec.product_id.name, rec.product_id.modelo_articulo or '', rec.product_uom_qty)
                res.append((rec.id, name))
            return res
        return super().name_get()


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    distributed = fields.Boolean(
        string='distributed',
    )
    distribute_ids = fields.One2many(
        'stock.distribute',
        'picking_id',
        string='Distribut',
    )


