# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    restrict_counrty_ids = fields.Many2many(related='website_id.restrict_counrty_ids',
                                            relation='res.country', readonly=False,
                                            string='Restrict User From Country')
