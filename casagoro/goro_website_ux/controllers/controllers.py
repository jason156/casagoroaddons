# -*- coding: utf-8 -*-
# from odoo import http


# class GoroWebsiteUx(http.Controller):
#     @http.route('/goro_website_ux/goro_website_ux/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/goro_website_ux/goro_website_ux/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('goro_website_ux.listing', {
#             'root': '/goro_website_ux/goro_website_ux',
#             'objects': http.request.env['goro_website_ux.goro_website_ux'].search([]),
#         })

#     @http.route('/goro_website_ux/goro_website_ux/objects/<model("goro_website_ux.goro_website_ux"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('goro_website_ux.object', {
#             'object': obj
#         })
