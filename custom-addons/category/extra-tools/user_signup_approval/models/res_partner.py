# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, _


class Partners(models.Model):
    _inherit = 'res.partner'

    last_name = fields.Char()