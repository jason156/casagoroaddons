# -*- coding: utf-8 -*-


from odoo import api, models, tools
from timeit import default_timer as timer

import logging
_logger = logging.getLogger(__name__)


class View(models.Model):
    _inherit = 'ir.ui.view'

    # apply ormcache_context decorator unless in dev mode...
    @api.model
    @tools.conditional(
        'xml' not in tools.config['dev_mode'],
        tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'view_id',
                       'tuple(self._context.get(k) for k in self._read_template_keys())'),
    )
    
    def _read_template(self, view_id):
        if 'xml' in tools.config['dev_mode']:
            return super(View, self)._read_template(view_id)

        start = timer()
        res = super(View, self)._read_template(view_id)
        _logger.info('Probably would have saved {:f}ms'.format((timer() - start) * 1000))

        return res
