odoo.define('ks_ecommerce_theme.product_multi_slider_base', function(require) {
    "use strict";

    var session = require('web.session');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var animation = require('website.content.snippets.animation');
    var core = require('web.core');
    var website = require('website.utils');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/ks_theme_kinetik/static/src/xml/ks_product_slider.xml', qweb);
    var WebsiteSaleProductSlider = Widget.extend({
        events: {},

        init: function(parent, id) {
            this._super(parent);
        },

        start: function() {
              this._super();

        }
    });

    animation.registry.website_sale_product_slider = animation.Class.extend({
        selector: ".ks_product_slider_multiple",
        widget: null,
        disabledInEditableMode: false,
        template: 'ks_snippet_product_slider',
        xmlDependencies: ['/ks_theme_kinetik/static/src/xml/ks_product_slider.xml'],

        ks_handleRecords:function(data,$target){
         var ks_rtl=data['rtl']
          var $inner_temp = $(qweb.render('ks_snippet_product_slider', {
                 "products": data,
               }));
               if($target){
                   $inner_temp.appendTo($target.empty());
                   var slider_id = "#"+data.slider_id;
                   var sliders = $(slider_id)
                   _.each(sliders,function(slider){
                          $(slider).owlCarousel({
                              items:data.items,
                              autoplay:data.auto_slide,
                              autoplayTimeout:data.speed,
                              autoplayHoverPause:true,
                              margin:30,
                              rtl:ks_rtl,
                              loop:data.loop,
                              nav:data.navs,
                              navText:['<i class="fa fa fa-angle-left"></i>','<i class="fa fa fa-angle-right"></i>'],
                              responsiveClass: true,
                              responsive:{
                                    0:{
                                        items: 2,
                                        dots: true,
                                        margin:10,
                                    },
                                    540:{
                                        items: 2,
                                        dots: true,
                                    },
                                    960:{
                                        items: 3,
                                        dots: true
                                    },
                                    1200:{
                                        items: data.items,
                                    }
                                },

                           })
                   });
               }
        },
        start: function(slider_id,ks_self_recived) {
            var ks_self = this;

            if(ks_self_recived !== undefined){
                ks_self = ks_self_recived;
                ks_self.$target.attr('data-id', slider_id);
                this.$el = ks_self_recived.$el;
                this.$target = ks_self_recived.$target;
                this.data = ks_self_recived.data;
                this.overlay = ks_self_recived.overlay;
            }
            var $target = ks_self.$target;
            var id = ks_self.$target.attr('data-id');

            if (!id) {
                return;
            }

            ajax.jsonRpc("/product/data", 'call', {"snippet_name":"slider","id":id}).then(function (data) {
                    this.ks_handleRecords(data,$target);
            }.bind(this));

        },
        stop: function() {
            this.widget.destroy();
        }
    });

});