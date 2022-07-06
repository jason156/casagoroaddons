from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_drop_zero_reserved(self):
        moves_to_drop = self.env['stock.move']

        zero_moves = self.move_lines.filtered(lambda move: move.reserved_availability == 0.0
                                              and move.state in ['draft', 'waiting', 'confirmed']
                                              and move.quantity_done == 0.0)
        if len(zero_moves):
            moves_to_drop = zero_moves + zero_moves._get_childs_to_drop()
            moves_to_drop._clean_merged()
            moves_to_drop._action_cancel()
            moves_to_drop.sudo().unlink()


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_childs_to_drop(self):

        childs_to_drop = self.mapped('move_dest_ids').filtered(lambda move: move.reserved_availability == 0.0
                                                               and move.quantity_done == 0.0)
        if len(childs_to_drop):
            childs_to_drop = childs_to_drop + childs_to_drop._get_childs_to_drop()
        return childs_to_drop
