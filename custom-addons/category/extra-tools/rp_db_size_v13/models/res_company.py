# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    database_size = fields.Char(string="Database Size", compute="_get_db_size")

    @api.depends('name', 'partner_id')
    def _get_db_size(self):
        db_name = self._cr.dbname
        # pg_database_size: return size in bytes
        # pg_size_pretty: return size in human-readable form (UNITS)
        self._cr.execute('''
            SELECT pg_size_pretty(pg_database_size(db.datname)) 
            FROM pg_database AS db 
            WHERE datname = %s ''', (db_name,))
        db_size = self._cr.fetchone()
        self.database_size = db_size[0]

    def get_table_size(self):
        self._cr.execute('''
            SELECT row_number() over (ORDER BY pg_total_relation_size (c.oid)) as serial_no, c.relname , pg_size_pretty(pg_total_relation_size(c.oid)), c.relnamespace
            FROM pg_class AS c
            LEFT JOIN pg_namespace n ON (n.oid = c.relnamespace)
            WHERE nspname NOT IN %s AND c.relkind <> %s AND nspname !~ %s
            ORDER BY pg_total_relation_size (c.oid) DESC''', ([('pg_catalog','information_schema'),'i','^pg_toast']))
        size_of_table = self._cr.fetchall()
        relation_model = self.env['relation.table.size'].sudo().search([])
        if len(relation_model):
            self._cr.execute('TRUNCATE TABLE relation_table_size')
        for rec in size_of_table:
            self.env['relation.table.size'].sudo().create({
                'name': rec[1],
                'size': rec[2]
            })
        view_id = self.env.ref('rp_db_size_v13.relation_table_size_tree').id,
        return {
            'name': ('Table Size'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'views': [[view_id, 'list']],
            'res_model': 'relation.table.size',
            'target': 'current',
        }


class EachTableSize(models.Model):
    _name = 'relation.table.size'
    _description = "Get Size of each table of currect db"


    name = fields.Char(string="Table Name")
    size = fields.Char(string="Size")


