# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models

class Website(models.Model):
    _inherit = "website"

    restrict_counrty_ids = fields.Many2many('res.country', 'website_country_rel',
                                            'website_id', 'country_id',
                                            string='Restrict User From Country')
