# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, Response
import logging
_logger = logging.getLogger(__name__)

class Home(http.Controller):
     
    @http.route(['/web/update_product_template'], type='http', auth='public', csrf=False)
    def update_product_template(self, **post):
        template_str = post.get('template_id')
        product_str = post.get('product_id')
        if template_str and product_str:
            try:
                template_id = template_str.split("-")[0]
                product_id = product_str.split("-")[0]
                product_obj = request.env['product.product'].browse(int(product_id))
                initial_template = product_obj.product_tmpl_id
                product_obj.with_context({'create_product_product':False}).write({
                    'product_tmpl_id':int(template_id),
                })
                template_obj = request.env['product.template'].browse(int(template_id))
                
                product_obj = product_obj.with_context({'variant_manager':True})
                template_obj = template_obj.with_context({'variant_manager':True})
                initial_template = initial_template.with_context({'variant_manager':True})
                if template_obj and product_obj:
                    
                    for attribute in product_obj.product_template_attribute_value_ids.mapped('product_attribute_value_id'):
                        if attribute.id not in template_obj.attribute_line_ids.mapped('value_ids').ids:
                            # Check there is line or not
                            if attribute.attribute_id.id in template_obj.attribute_line_ids.mapped('attribute_id').ids:
                                # Line is there
                                attribute_line = template_obj.attribute_line_ids.filtered(lambda x : x.attribute_id.id == attribute.attribute_id.id)
                                attribute_line.sudo().with_context({'variant_manager':True}).write({
                                    'value_ids':[(4,attribute.id)]
                                })
                            else:
                                request.env['product.template.attribute.line'].sudo().with_context({'variant_manager':True}).create({
                                    'product_tmpl_id':template_obj.id,
                                    'attribute_id':attribute.attribute_id.id,
                                    'value_ids':[(6,0,attribute.ids)]
                                })
                    
                    # Remove attribute value if not used in any of the variant anymore
                    for attribute in product_obj.product_template_attribute_value_ids.mapped('product_attribute_value_id'):
                        if attribute.id not in initial_template.product_variant_ids.mapped('product_template_attribute_value_ids').mapped('product_attribute_value_id').ids:
                            for attribute_line in initial_template.attribute_line_ids:
                                if attribute.id in attribute_line.value_ids.ids:
                                    if len(attribute_line.value_ids) == 1:
                                        attribute_line.sudo().unlink()
                                    else:
                                        attribute_line.sudo().write({
                                            'value_ids':[(3,attribute.id)]
                                        })
                                        
                    # Remove empty line from initial Template
                    for attribute_line in initial_template.attribute_line_ids:
                        if not attribute_line.value_ids:
                            attribute_line.sudo().unlink()

                    initial_template.attribute_line_ids._update_product_template_attribute_values()
                    template_obj.attribute_line_ids._update_product_template_attribute_values()
   
                    for ptav in product_obj.product_template_attribute_value_ids:
                        destination_values = request.env['product.template.attribute.value'].with_context({'active_test':False}).search([
                            ('product_tmpl_id','=',template_obj.id),
                            ('product_attribute_value_id','=',ptav.product_attribute_value_id.id),
                        ],limit=1)
                        if destination_values:
                            if not destination_values.ptav_active:
                                destination_values.write({
                                    'ptav_active':True,
                                })
                            
                            product_obj.write({
                                'product_template_attribute_value_ids': [(3,ptav.id),(4,destination_values.id)]
                            })

                    attribute_values = request.env['product.template.attribute.value'].with_context({'active_test':False}).search([('product_tmpl_id','=',initial_template.id)])
                    for ptav in attribute_values:
                        if not ptav.ptav_product_variant_ids.ids:
                            ptav.sudo().with_context({'attribute_manager':True}).unlink()

                template_obj._compute_product_variant_count()
                initial_template._compute_product_variant_count()
                return request.make_response("data;;;$#template-badge-%s;;;$%s;;;$#template-badge-%s;;;$%s;;;$#%s-variant-name;;;$%s"%(initial_template.id,initial_template.product_variant_count,template_obj.id,template_obj.product_variant_count,product_obj.id,product_obj.display_name))
            except Exception as e:
                _logger.info(e)
                return request.make_response("There is some problem with re-mapping products. Please refresh page and try again.")
        
        return request.make_response("There is some problem with re-mapping products. Please refresh page and try again.")
    