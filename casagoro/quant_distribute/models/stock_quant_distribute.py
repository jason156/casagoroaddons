from odoo import fields, models, api
import logging
import math

_logger = logging.getLogger(__name__)


class QuantDistribute(models.Model):
    _name = 'stock.quant.distribute'
    _description = 'stock quant distribute'

    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
    location_parent_id = fields.Many2one(
        'stock.location',
        string='Location',
    )

    name = fields.Datetime(
        string='Date',
        default=lambda self: fields.Datetime.now()
    )
    state = fields.Selection(
        [('draft', 'draft'), ('distribute', 'distribute'),
         ('done', 'done'), ('cancel', 'cancel')],
        string='State',
        default='draft'
    )
    distribute_quants_ids = fields.One2many(
        'stock.distribute.quant',
        'distribute_id',
        string='Quants',
    )

    location_ids = fields.Many2many(
        'stock.location',
        string='Locations',

    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='warehouse',
        compute='compute_warehouse'
    )
    view_location_id = fields.Many2one(
        'stock.location',
        string='parent location',
        compute='compute_warehouse'
    )

    items_ids = fields.One2many(
        'stock.quant.distribute.item',
        'distribute_id',
        string='Items',
    )

    def add_quant_clear(self):
        self.add_quant()
        self.product_id = False

    def add_quant(self):
        quants = self.env['stock.quant'].search([
            ('location_id', 'child_of', self.location_parent_id.id),
            ('product_id', '=', self.product_id.id),
            ('quantity', '>', 0),
        ]).filtered(lambda x: x.quantity > x.reserved_quantity)
        if len(quants):

            new_quant = quants - self.distribute_quants_ids.mapped('quant_id')
            if len(new_quant):
                self.distribute_quants_ids = [(0, 0, {
                    'quant_id': q.id,
                    'distribute_quantity': q.quantity - q.reserved_quantity}
                ) for q in new_quant]

    def action_distribute(self):
        self.state = 'distribute'
        self.compute_warehouse()
        self.add_items()

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        if 'active_ids' in self._context:
            quants = self.env['stock.quant'].search(
                [('id', 'in', self._context['active_ids'])])
            distribute_quants_ids = [(0, 0, {
                'quant_id': q.id,
                'distribute_quantity': q.quantity - q.reserved_quantity}
            ) for q in quants]

            res.update({'distribute_quants_ids': distribute_quants_ids})
        return res

    def action_cancel(self):
        self.state = 'cancel'

    #@api.onchange('quant_ids')
    def compute_warehouse(self):
        if len(self.distribute_quants_ids):
            location_id = self.distribute_quants_ids.mapped('location_id')
            self.warehouse_id = location_id[0].get_warehouse().id

            self.view_location_id = self.warehouse_id.view_location_id.id
            if (self.view_location_id):
                self.location_ids = [(6, 0,
                                      self.env['stock.location'].search(
                                          [
                                              ('distribute', '=', True),
                                              ('id', 'child_of',
                                               self.view_location_id.id)
                                          ]).ids
                                      )
                                     ]
        else:
            self.warehouse_id = False
            self.view_location_id = False
            self.location_ids = False

    @api.onchange('state', 'distribute_quants_ids', 'location_ids')
    def add_items(self):
        if self.state != 'distribute':
            return
        self.items_ids = False
        loc = self.env['stock.location'].search(
            [('id', 'in', self.location_ids.ids)], order="distribute_sequence asc")

        total = sum(loc.mapped('distribute_part'))
        location_count = len(loc)

        for quant in self.distribute_quants_ids:
            product_count = 0.0
            location_pos = 0
            _logger.info(quant)
            for location_id in loc:
                location_pos += 1
                disp = quant.distribute_quantity
                qty = math.floor((location_id.distribute_part * disp) / total)
                product_count += qty
                if location_pos == location_count and product_count < disp:
                    qty += disp - product_count
                self.env['stock.quant.distribute.item'].create({
                    'distribute_id': self.id,
                    'quant_id': quant.quant_id.id,
                    'location_id': location_id.id,
                    'qty': 0.0 + qty,
                })

    def action_create_pickings(self):
        pickings = {}
        # to-do: esto quedo desprolijo son dos variables con lo mismo
        picking_ids = self.env['stock.picking']

        int_type_id = self.warehouse_id.int_type_id.id
        #location_id = self.picking_id.location_dest_id.id

        for item in self.items_ids:
            if item.qty > 0.0:
                if str(item.location_id.id) not in pickings.keys():
                    exist_picking = self.env['stock.picking'].search([
                        ('location_id', '=', item.quant_id.location_id.id),
                        ('location_dest_id', '=', item.location_id.id),
                        ('immediate_transfer', '=', True),
                        ('state', 'in', ['confirmed', 'assigned'])
                    ], limit=1)
                    if len(exist_picking):
                        pickings[str(item.location_id.id)] = exist_picking
                        picking_ids += exist_picking
                    else:
                        pickings[str(item.location_id.id)] = self.env['stock.picking'].create({
                            'picking_type_id': int_type_id,
                            'location_id': item.quant_id.location_id.id,
                            'location_dest_id': item.location_id.id,
                            # 'move_line_ids_without_package': [],
                            'immediate_transfer': True,
                            'move_type': 'direct',
                        })
                        picking_ids += pickings[str(item.location_id.id)]

                pickings[str(item.location_id.id)].move_line_ids_without_package = [
                    (0, 0,
                     {
                         'product_id': item.quant_id.product_id.id,
                         'qty_done': item.qty,
                         'product_uom_id': item.quant_id.product_id.uom_id.id,
                         'location_id': item.quant_id.location_id.id,
                         'location_dest_id': item.location_id.id,
                     })
                ]

        for pick in picking_ids:
            pick.button_validate()
        ids = picking_ids.ids
        view_id = self.env.ref('stock.vpicktree').id
        self.name = fields.Datetime.now()
        self.state = 'done'

        return {
            'name': 'New picks',
            'view_type': 'tree,form',
            'view_mode': 'list',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', ids)],
            'target': 'new',
            'view_id': view_id
        }

    def open_distribute(self):
        view_id = self.env.ref('stock_distribute.stock_distribute_form').id
        return {
            'name': 'Distribute',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.distribute',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'view_id': view_id
        }


class StockDistributeQuant(models.Model):
    _name = 'stock.distribute.quant'
    _description = 'Description'

    distribute_id = fields.Many2one(
        'stock.quant.distribute',
        string='distribute',
    )

    quant_id = fields.Many2one(
        'stock.quant',
        string='quant',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        related="quant_id.product_id"
    )
    location_id = fields.Many2one(
        'stock.location',
        string='location',
        related="quant_id.location_id"
    )
    quantity = fields.Float(
        string='quantity',
        related="quant_id.quantity"
    )

    reserved_quantity = fields.Float(
        string='reserved',
        related="quant_id.reserved_quantity"
    )

    distribute_quantity = fields.Float(
        string='distribute',
    )

    @api.onchange('quant_id')
    def set_distribute_quantity(self):
        for res in self:
            res.distribute_quantity = res.quantity - res.reserved_quantity


class StockDistributeItem(models.Model):
    _name = 'stock.quant.distribute.item'
    _description = 'stock quant distribute item'

    distribute_id = fields.Many2one(
        'stock.quant.distribute',
        string='distribute',
    )
    name = fields.Char(
        string='name',
        compute="_compute_name"
    )
    quant_id = fields.Many2one(
        'stock.quant',
        string='Quant',
        ondelete='set null',
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        store=True,
    )
    loc_name = fields.Char(
        string='Location',
        compute="_compute_name",
        store=True,
    )
    qty = fields.Float(
        string='qty',
        digits='Product Unit of Measure',
    )

    @api.depends('quant_id')
    def _compute_name(self):
        for item in self:
            if item.quant_id:
                item.name = '%s %s' % (
                    item.quant_id.product_id.name, item.quant_id.quantity)
                item.loc_name = '%s' % (item.location_id.name)
