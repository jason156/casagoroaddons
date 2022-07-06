from odoo import fields, models
import re
import yaml

import logging

_logger = logging.getLogger(__name__)


class productMerge(models.TransientModel):
    _name = 'product.merge'
    _description = 'Merge products'

    state = fields.Selection(
        [('step_1', 'step 1'), ('step_2', 'step 2'), ('step_3', 'step 3')],
        string='Step',
        default='step_1'
    )
    base_template_id = fields.Many2one(
        'product.template',
        string='template',
    )
    pattern = fields.Char(
        string='Patron a buscar',
    )
    attribute_ids = fields.Many2many(
        'product.attribute',
        string='attributes',
    )
    product_ids = fields.Many2many(
        'product.product',
        string='products',
    )
    log = fields.Text(
        string='Log',
    )

    def action_back(self):
        self.state = 'step_1'

    def check_variants(self):
        mapping = []
        prog = r'%s' % self.pattern

        for product_id in self.product_ids:

            item = {'product_id': product_id.id,
                    'name': product_id.name, 'variant': []}
            result = re.search(prog, product_id.name)
            if result:
                i = 1
                for attr in self.attribute_ids:
                    item['variant'].append(
                        {'name': attr.name, 'id': attr.id, 'value': result.group(i)})
                    i += 1

            else:
                _logger.info(result)
            mapping.append(item)
        self.log = yaml.dump(mapping)
        self.state = 'step_2'

    def process_yalm(self):

        data = yaml.load(self.log)
        for product in data:
            product_id = self.env['product.product'].browse(
                product['product_id'])
            product_tmpl_id = product_id.product_tmpl_id
            if self.base_template_id.id != product_tmpl_id.id:
                product_tmpl_id.active = False
            value_ids = []
            for variant in product['variant']:
                variant_value = self.env['product.attribute.value'].search([
                    ('attribute_id', '=', variant['id']),
                    ('name', '=', variant['value'])])
                if not len(variant_value):
                    variant_value = self.env['product.attribute.value'].create({
                        'name': variant['value'],
                        'attribute_id': variant['id']
                    })

                attribute_line_id = self.env['product.template.attribute.line'].search(
                    [('product_tmpl_id', '=', self.base_template_id.id),
                     ('attribute_id', '=', variant['id'])
                     ]
                )
                if len(attribute_line_id) and variant_value.id not in attribute_line_id.ids:
                    attribute_line_id.with_context(
                        ignore_create_variant=True).write({
                            'value_ids': [(4, variant_value.id)]
                        })
                elif not len(attribute_line_id):
                    attribute_line_id = self.env['product.template.attribute.line'].with_context(
                        ignore_create_variant=True).create({
                            'product_tmpl_id': self.base_template_id.id,
                            'attribute_id': variant['id'],
                            'value_ids': [(4, variant_value.id)]
                        })
                value_ids.append(variant_value.id)

            try:
                attribute_value_ids = self.env['product.template.attribute.value'].search(
                    [('product_tmpl_id', '=', self.base_template_id.id), ('product_attribute_value_id', 'in', value_ids)])
                product_id.with_context(update_product_template_attribute_values=False).write({
                    'product_template_attribute_value_ids': [(6, 0, attribute_value_ids.ids)],
                    'product_tmpl_id': self.base_template_id.id,
                    'active': True
                })

            except Exception as e:
                _logger.info(e)
            self.env.cr.commit()
        self.state = 'step_3'


class ProductTemplate(models.Model):

    _inherit = "product.template"

    def _create_variant_ids(self):
        if self.env.context.get('ignore_create_variant', False):
            return True
        return super()._create_variant_ids()
