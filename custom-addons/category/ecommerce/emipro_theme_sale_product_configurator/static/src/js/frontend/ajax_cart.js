odoo.define('emipro_theme_sale_product_configurator.ajax_cart', function (require) {
    "use strict";
    /*var sAnimations = require('website.content.snippets.animation');
    var core = require('web.core');*/
    var publicWidget = require('web.public.widget');
     var ajax = require('web.ajax');
    /*var _t = core._t;
    var WebsiteSale = new sAnimations.registry.WebsiteSale();
    var QWeb = core.qweb;
    var xml_load = ajax.loadXML(
        '/website_sale_stock/static/src/xml/website_sale_stock_product_availability.xml',
        QWeb
    );*/
    var OptionalProductsModal = require('sale_product_configurator.OptionalProductsModal');
    var flag = 1;

    OptionalProductsModal.include({
    /** Ajax cart for the optional product popup */
        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.isWebsite = params.isWebsite;

            this.dialogClass = 'oe_optional_products_modal' + (params.isWebsite ? ' oe_website_sale' : '');
            setTimeout(function(){
                if($('.oe_optional_products_modal').length && $('#ajax_cart_template').val() == 1) {
                    var ajaxCart = new publicWidget.registry.ajax_cart();
                    if(!parent.attr('class')) {
                        var product_id = $('.oe_optional_products_modal').find('.product_template_id').val();
                        $(document).on('click', '.modal-footer .btn-secondary', function(){
                            ajaxCart.ajaxCartSucess(product_id);
                        });
                    } else {
                         var optional_parent = parent.attr('class')
                        optional_parent = optional_parent.replace(" ", ".");
                        var modal_id = $('.'+optional_parent).find('.modal_shown').attr('id');
                        var product_id = $('#'+modal_id).find('.product_template_id').val();
                        $(document).on('click', '#'+modal_id+' .modal-footer .btn-secondary', function(){
                            ajaxCart.ajaxCartSucess(product_id);
                        });
                    }
                }
            },800);
        }
    });

});
