# -*- coding: utf-8 -*-

from odoo import api ,models, fields , _
from odoo.exceptions import Warning

class Pos_Config_Inherit(models.Model):
	_inherit = "pos.config"

	is_pos_shop_keyboard = fields.Boolean(string = "Enable for POS Shop Keyboard shortcut")
	is_pos_restaurant_keyboard = fields.Boolean(string = "Enable for POS Restaurant Keyboard shortcut")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
