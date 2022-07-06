from odoo import fields, models, api
import logging
import math

_logger = logging.getLogger(__name__)


class StockDistribute(models.Model):
    _name = 'stock.distribute'
    _description = 'stock.distribute'

    name = fields.Datetime(
        string='Date',
        default=lambda self: fields.Datetime.now()
    )
    state = fields.Selection(
        [('draft', 'draft'), ('done', 'done'), ('cancel', 'cancel')],
        string='State',
        default='draft'
    )
    picking_id = fields.Many2one(
        'stock.picking',
        string='Picking',
        required=True,
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
        'stock.distribute.item',
        'distribute_id',
        string='Items',
    )

    def action_cancel(self):
        self.state = 'cancel'

    @api.onchange('picking_id')
    def compute_warehouse(self):
        if len(self.picking_id):
            self.warehouse_id = self.picking_id.location_dest_id.get_warehouse().id
            self.view_location_id = self.warehouse_id.view_location_id.id
            self.location_ids = [(6, 0,
                                  self.env['stock.location'].search(
                                      [
                                          ('distribute', '=', True),
                                          ('id', 'child_of',
                                           self.view_location_id.id)
                                      ]).ids
                                  )
                                 ]
            self.warehouse_id = self.picking_id.location_dest_id.get_warehouse().id

    @api.onchange('picking_id', 'location_ids')
    def add_items(self):
        self.items_ids = False
        loc = self.env['stock.location'].search(
            [('id', 'in', self.location_ids.ids)], order="distribute_sequence asc")

        to_distribute = self.picking_id.move_lines.filtered(
            lambda x: x.product_uom_qty > x.distributed_qty)
        for move in to_distribute:
            location_pos = 0
            for location_id in loc:
                location_pos += 1

                self.env['stock.distribute.item'].create({
                    'distribute_id': self.id,
                    'move_id': move.id, 
                    'location_id': location_id.id,
                    'qty': 0.0 ,
                })

    def action_create_pickings(self):
        pickings = {}
        if len(self.picking_id.picking_type_id.warehouse_id.intr_type_id):
            int_type_id = self.picking_id.picking_type_id.warehouse_id.intr_type_id.id
        else:
            int_type_id = self.picking_id.picking_type_id.warehouse_id.out_type_id.id
        location_id = self.picking_id.location_dest_id.id
        all_lines = True
        for item in self.items_ids:
            if item.qty > 0.0:
                if str(item.location_id.id) not in pickings.keys():
                    pickings[str(item.location_id.id)] = {
                        'picking_type_id': int_type_id,
                        'location_id': location_id,
                        'location_dest_id': item.location_id.id,
                        'move_lines': [],
                        # 'immediate_transfer': False,
                        # 'move_type': 'one',
                        'state': 'draft',
                    }
                    #picking_ids += pickings[str(item.location_id.id)]

                pickings[str(item.location_id.id)]['move_lines'].append(
                    (0, 0,
                     {
                         'name': item.move_id.product_id.display_name,
                         'product_id': item.move_id.product_id.id,
                         'product_uom_qty': item.qty,
                         'product_uom': item.move_id.product_uom.id,
                         'location_id': location_id,
                         'location_dest_id': item.location_id.id,
                     })
                )
                item.move_id.distributed_qty += item.qty
            else:
                all_lines = False
        picking_ids = self.env['stock.picking'].create(pickings.values())
        for pick in picking_ids:
            pick.action_confirm()
            pick.action_assign()

        ids = picking_ids.ids
        view_id = self.env.ref('stock.vpicktree').id
        if all_lines:
            self.picking_id.distributed = True
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

    def action_create_pickings_inmediate(self):
        pickings = {}
        # to-do: esto quedo desprolijo son dos variables con lo mismo
        picking_ids = self.env['stock.picking']

        int_type_id = self.picking_id.picking_type_id.warehouse_id.int_type_id.id
        _logger.info("int_type_id %r" % int_type_id)
        location_id = self.picking_id.location_dest_id.id
        all_lines = True
        for item in self.items_ids:
            if item.qty > 0.0:
                if str(item.location_id.id) not in pickings.keys():
                    exist_picking = self.env['stock.picking'].search([
                        ('location_id', '=', location_id),
                        ('location_dest_id', '=', item.location_id.id),
                        ('immediate_transfer', '=', True),
                        ('state', 'in', ['confirmed', 'assigned'])
                    ], limit=1)
                    if len(exist_picking):
                        pickings[str(item.location_id.id)] = exist_picking
                        picking_ids += exist_picking
                    else:
                        pickings[str(item.location_id.id)] = self.env['stock.picking'].with_context(
                            default_immediate_transfer=True
                        ).create({
                            'picking_type_id': int_type_id,
                            'location_id': location_id,
                            'location_dest_id': item.location_id.id,
                            # 'move_line_ids_without_package': [],
                            'immediate_transfer': True,
                            'move_type': 'direct',
                        })
                        picking_ids += pickings[str(item.location_id.id)]

                pickings[str(item.location_id.id)].with_context(
                    default_immediate_transfer=True
                ).move_line_ids_without_package = [
                    (0, 0,
                     {
                         'product_id': item.move_id.product_id.id,
                         'qty_done': item.qty,
                         'product_uom_id': item.move_id.product_uom.id,
                         'location_id': location_id,
                         'location_dest_id': item.location_id.id,
                     })
                ]
                item.move_id.distributed_qty += item.qty
            else:
                all_lines = False

        # for pick in picking_ids:
        #    pick.with_context(
        #        default_immediate_transfer=True
        #    ).button_validate()
        ids = picking_ids.ids
        view_id = self.env.ref('stock.vpicktree').id
        if all_lines:
            self.picking_id.distributed = True
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


class StockDistributeItem(models.Model):
    _name = 'stock.distribute.item'
    _description = 'stock distribute item'

    distribute_id = fields.Many2one(
        'stock.distribute',
        string='distribute',
    )
    name = fields.Char(
        string='name',
        compute="_compute_name"
    )
    move_id = fields.Many2one(
        'stock.move',
        string='Move',
        required=True,
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Location',
    )
    loc_name = fields.Char(
        string='Location',
        compute="_compute_name"
    )
    qty = fields.Float(
        string='qty',
        digits='Product Unit of Measure',
    )

    @api.depends('move_id')
    def _compute_name(self):
        for item in self:
            item.name = '%s %s' % (
                item.move_id.product_id.name, item.move_id.product_uom_qty)
            item.loc_name = '%s' % (item.location_id.name)
