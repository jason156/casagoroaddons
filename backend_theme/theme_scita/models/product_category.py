# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools
from odoo.addons.website_sale.controllers import main


class ProductPublicCategory(models.Model):

    _inherit = 'product.public.category'

    linked_product_count = fields.Integer(string='# of Productos')
    include_in_megamenu = fields.Boolean(
        string="Incluir en mega menú", help="Incluir en mega menú")
    menu_id = fields.Many2one('website.menu', string="Main menu")
    description = fields.Text(string="Descripción",
                              translate=True,
                              help="""Breve descripción que será
                              visible debajo del control deslizante de categoría.""")

# for product tag


class ProductTags(models.Model):
    _name = 'biztech.product.tags'
    _order = "sequence"
    _description = 'Etiquetas de productos'

    name = fields.Char(string="Nombre de etiqueta", help="Nombre de etiqueta",
                       required=True, translate=True)
    active = fields.Boolean(
        string="Active", help="Habilitar o deshabilitar la etiqueta del sitio web", default=True)
    sequence = fields.Integer(
        string="Sequence", help="Puede definir la secuencia de etiquetas que desea mostrar etiquetas")
    product_ids = fields.Many2many(
        'product.template', string='Productos', required=True)

    _sql_constraints = [('unique_tag_name', 'unique(name)',
                         'El nombre de la etiqueta debe ser único ..!'), ]


class ProductStyleTags(models.Model):
    _name = 'biztech.product.style.tag'
    _description = 'Etiquetas de estilo de producto'

    name = fields.Char(string='Nombre de etiqueta', required=True, translate=True)
    color = fields.Selection(
        [('blue', 'Azul'), ('red', 'Rojo'), ('yellow', 'Amarillo'), ('brown', 'Marron')], string="Color")
    product_ids = fields.One2many(
        'product.template',
        'product_style_tag_id',
        string='Product Tags',
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one(
        'product.brands',
        string='Marca',
        help='Seleccione una marca para este producto'
    )
    tag_ids = fields.Many2many('biztech.product.tags', string="Etiquetas de productos")
    multi_image = fields.Boolean(string="¿Agregar varias imágenes?")
    product_style_tag_id = fields.Many2one(
        'biztech.product.style.tag',
        string='Tags',
        help='Seleccione una etiqueta para este producto'
    )
    biz_images = fields.One2many('scita.product.images', 'biz_product_tmpl_id',
                                 string='Imágenes del producto')
    deal_product = fields.Boolean(string='Disponible para oferta del día')

    def quick_publish_product(self):
        self.ensure_one()
        self.is_published = not(self.is_published)

    def action_product_publish(self):
        self.is_published = True

    def action_product_unpublish(self):
        self.is_published = False
        
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    def quick_publish_product(self):
        self.ensure_one()
        self.is_published = not(self.is_published)

    def action_product_publish(self):
        self.is_published = True

    def action_product_unpublish(self):
        self.is_published = False

class Brands(models.Model):
    _name = 'product.brands'
    _description = 'Marcas de productos'
    _order = "sequence"

    active = fields.Boolean(
        string="Active", default=True, help="""Si esta Activo se mostrarán las marcas""")
    sequence = fields.Integer()
    name = fields.Char(string='Nombre Marca', required=True, translate=True)
    brand_description = fields.Text(string='Description', translate=True)
    image = fields.Binary(string='Brand Logo', attachment=True,)
    image_medium = fields.Binary("Medium-sized Image", attachment=True,
                                 help="Medium-sized logo of the brand. It is automatically "
                                 "resized as a 128x128px image, with aspect ratio preserved. "
                                 "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized Image", attachment=True,
                                help="Small-sized logo of the brand. It is automatically "
                                "resized as a 64x64px image, with aspect ratio preserved. "
                                "Use this field anywhere a small image is required.")
    brand_cover = fields.Binary(string='Brand Cover', attachment=True,)
    product_ids = fields.One2many(
        'product.template',
        'product_brand_id',
        string='Marcas Productos',
    )
    products_count = fields.Integer(
        string='Número de productos',
        compute='_get_products_count',
    )

    _sql_constraints = [('unique_tag_name', 'unique(name)',
                         'Brands name should be unique..!'), ]

    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)


class ProductSortBy(models.Model):
    _name = 'biztech.product.sortby'
    _description = 'Custom Product Sorting'

    name = fields.Char(string="Name", help='Name for sorting option',
                       required=True)
    sort_type = fields.Selection(
        [('asc', 'Ascending'), ('desc', 'Descending')], string="Type", default='asc')
    sort_on = fields.Many2one('ir.model.fields', string='Sort On',
                              help='Select field on which you want to apply sorting',
                              domain=[('model', '=', 'product.template'),
                                      ('ttype', 'in',
                                       ('char', 'float', 'integer', 'datetime', 'date'))])


class ProductPerPageNo(models.Model):
    _name = "product.per.page.no"
    _order = 'name asc'
    _description = "Add page no"

    name = fields.Integer(string='Producto por página')
    set_default_check = fields.Boolean(string="Set default")
    prod_page_id = fields.Many2one('product.per.page')

    @api.model
    def create(self, vals):
        res = super(ProductPerPageNo, self).create(vals)
        if vals.get('name') == 0:
            raise Warning(
                _("¡Advertencia! No puede establecer 'cero' para la página del producto."))
        if vals.get('set_default_check'):
            true_records = self.search(
                [('set_default_check', '=', True), ('id', '!=', res.id)])
            true_records.write({'set_default_check': False})
        return res

    def write(self, vals):
        res = super(ProductPerPageNo, self).write(vals)
        if vals.get('name') == 0:
            raise Warning(
                _("¡Advertencia! No puede establecer 'cero' para la página del producto."))
        if vals.get('set_default_check'):
            true_records = self.search(
                [('set_default_check', '=', True), ('id', '!=', self.id)])
            true_records.write({'set_default_check': False})
        return res


class ProductPerPage(models.Model):
    _name = "product.per.page"
    _description = "Agregue número de exhibición del producto en una página"

    name = fields.Char(string="Label Name", translate=True)
    no_ids = fields.One2many(
        'product.per.page.no', 'prod_page_id', string="Número de producto para mostrar")

    def write(self, vals):
        res = super(ProductPerPage, self).write(vals)
        default_pg = self.env['product.per.page.no'].search(
            [('set_default_check', '=', True)])
        if default_pg.name:
            main.PPG = int(default_pg.name)
        else:
            raise Warning(
                _("¡Advertencia! Debe establecer al menos un valor predeterminado."))
        return res


class ScitaMultiProductImages(models.Model):
    _name = 'scita.product.images'
    _description = "Agregar varias imágenes en el producto"

    name = fields.Char(string='Title', translate=True)
    alt = fields.Char(string='Alt', translate=True)
    attach_type = fields.Selection([('image', 'Image'), ('video', 'Video')],
                                   default='image',
                                   string="Type")
    image = fields.Binary(string='Image', store=True, attachment=True)
    video_type = fields.Selection([('youtube', 'Youtube'),
                                   ('vimeo', 'Vimeo'),
                                   ('html5video', 'Html5 Video')],
                                  default='youtube',
                                  string="Video media player")
    cover_image = fields.Binary(string='Cover image', store=True, attachment=True,
                                help="Cover Image will be show untill video is loaded.")
    video_id = fields.Char(string='Video ID')
    video_ogv = fields.Char(
        string='Video OGV', help="Link for ogv format video")
    video_webm = fields.Char(
        string='Video WEBM', help="Link for webm format video")
    video_mp4 = fields.Char(
        string='Video MP4', help="Link for mp4 format video")
    sequence = fields.Integer(string='Sort Order')
    biz_product_tmpl_id = fields.Many2one('product.template', string='Product')
    more_view_exclude = fields.Boolean(string="More View Exclude")

class Zipcodes(models.Model):
    _name = 'delivery.zipcode'
    _description = "Configuración del código postal del área de entrega"
    
    name = fields.Char(string='C.Postal', required=True)