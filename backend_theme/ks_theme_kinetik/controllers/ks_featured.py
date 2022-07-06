from odoo import http
from odoo.http import request


class WebsiteShopFeatured(http.Controller):
    """Fectching products on the basis of the tags"""

    @http.route([
        '/product/featured',
    ], type='json', auth="public", website=True)
    def product_featured_home_page(self):
        products = []
        trendy_id, new_arr_id, ks_popular, ks_classics = self.get_tags()
        featured_prods = request.env['product.template'].search(
            ["|", "|", "|", ("ks_product_tags", "=", ks_classics.id),
             ("ks_product_tags", "=", ks_popular.id),
             ("ks_product_tags", "=", trendy_id.id),
             ("ks_product_tags", "=", new_arr_id.id),
             ("is_published", "=", True)
             ])
        vals = {
            'trendy_tag_name': trendy_id.name,
            'ks_trendy_count': len(trendy_id.ks_product_ids),
            'new_arrvd_tag_name': new_arr_id.name,
            'new_arr_id_count': len(new_arr_id.ks_product_ids),
            'ks_populae_tag_name': ks_popular.name,
            'ks_popular_count': len(ks_popular.ks_product_ids),
            'ks_classics_tag_name': ks_classics.name,
            'ks_classics_count': len(ks_classics.ks_product_ids),
        }
        products.append(vals)
        ks_currency_id = request.env['website'].get_current_website().currency_id
        for prods in featured_prods:
            is_trendy = trendy_id.id in prods.ks_product_tags.ids
            is_new_arrvd = new_arr_id.id in prods.ks_product_tags.ids
            is_ks_popular = ks_popular.id in prods.ks_product_tags.ids
            is_ks_classics = ks_classics.id in prods.ks_product_tags.ids

            ks_img_url = "/web/image/product.template/" + str(prods.id) + "/image_256"
            ks_product_var_id = prods['product_variant_id'].id

            is_ks_wishlist = request.website.viewref('website_sale_wishlist.add_to_wishlist').active
            is_ks_cart = request.website.viewref('website_sale.products_add_to_cart').active
            is_ks_compare = request.website.viewref('website_sale_comparison.add_to_compare').active
            is_ks_product_det = request.website.viewref('website_sale.products_description').active
            prod_price = prods._get_combination_info(prods._get_first_possible_combination(), add_qty=1, pricelist='')['list_price']
            if not prod_price:
                prod_price = prods['list_price']
            values = {
                'product_name': prods.name,
                'product_img': ks_img_url,
                'prod_id': prods.id,
                 'website_price':  float("{0:.2f}".format(prod_price)),
                'description_sale': prods.description_sale,
                'prod_brand': prods.id,
                'product': prods,
                'website_public_price':prod_price ,
                'website_currency_id': ks_currency_id.symbol,
                'website_currency_position': ks_currency_id.position,
                'prod_price': float("{0:.2f}".format(prods.list_price)),
                'is_trendy': is_trendy,
                'is_new_arrvd': is_new_arrvd,
                'is_ks_popular': is_ks_popular,
                'is_ks_classics': is_ks_classics,
                'brand_name': prods.ks_product_brand_id.name,
                'ks_product_var_id': ks_product_var_id,
                'is_ks_wishlist': is_ks_wishlist,
                'is_ks_cart': is_ks_cart,
                'is_ks_compare': is_ks_compare,
                'is_ks_product_det': is_ks_product_det,
                'prod_url': "/shop/product/%s" % (prods['id'],),
            }
            products.append(values)
        return products

    # This return hard coded tags
    # Add more tags in the search what if user create a tag?
    def get_tags(self):
        trendy_id = request.env.ref('ks_theme_base.ks_products_tags_trendy')
        new_arr_id = request.env.ref('ks_theme_base.ks_products_tags_new_arrival')
        ks_popular = request.env.ref('ks_theme_base.ks_products_tags_Most_popular')
        ks_classics = request.env.ref('ks_theme_base.ks_products_tags_Classics')
        return trendy_id, new_arr_id, ks_popular, ks_classics
