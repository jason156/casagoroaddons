# Powered by SCRIMO GmbH  - Roman Weinberger 2019
# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def set_as_customer(self):
        self.customer_rank = 1

    def set_notas_customer(self):
        self.customer_rank = 0

    def set_as_vendor(self):
        self.supplier_rank = 1

    def set_notas_vendor(self):
        self.supplier_rank = 0