# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Config(models.Model):
    _inherit = 'pos.config'

    module_test_operations = fields.Boolean('Test/Sample Orders')
