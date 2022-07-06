odoo.define('ks_ecommerce_theme.product_slider_multi_tab', function(require) {
    "use strict";

    var session = require('web.session');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var ks_widget = require('web_editor.widget');
    var animation = require('website.content.snippets.animation');
    var core = require('web.core');
    var website = require('website.utils');
    var options = require('web_editor.snippets.options');
    var ks_website_slider = require('ks_ecommerce_theme.product_multi_slider_base');
//    var multitab_slider_js=ajax.loadJS("/ks_theme_kinetik/static/src/js/snippets/ks_product_multi_slider_base.js");
    var _t = core._t;
    var qweb = core.qweb;
    var ks_SnippetSelectionDialog = ks_widget.Dialog.extend({
        start: function() {
             var ks_self = this;
             ks_self.ks_setData(ks_self);
             ks_self._super();
        },
        ks_setData:function(modal){
                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                        model: 'ks_product.multitab_slider',
                        method: 'search_read',
                        args: [],
                        kwargs: {
                            fields: ['name'],
                        }
                    }).then(function(data){
                     var select = $("<select></select>").attr("id", "ks_slider_selection").attr("name", "Selection slider");
                      $.each(data,function(index,json){
                       var ks_slider_id = "#product-owl-id-"+(json.id)
//                       if($(ks_slider_id).length === 0){
                         select.append($("<option></option>").attr("value", json.name).attr("id", json.id).text(json.name));
//                       }
                     });
                     $(modal.$el).append(select[0]);

                 });

        },
     });
    options.registry.product_slider_actions_multitab = options.Class.extend({
        on_prompt:function(ks_self){
                var dialog = new ks_SnippetSelectionDialog(ks_self, {
                    title: _t('Select Slider'),
                });
                dialog.open();
                dialog.on('save', this, function () {
                     var slider_id =  $('#ks_slider_selection').find(":selected").attr("id");
//                     multitab_slider_js.then(function(){
                     var ks_new_slider = new animation.registry.website_sale_mutitab_product_slider_1(ks_self);
//                     })
                     ks_new_slider.start(slider_id,ks_self);

                });
                dialog.on('cancel', this,function () {
                       this.$target.remove();
                });

        },
        onBuilt: function() {
                var ks_self = this;
                ks_self.on_prompt(ks_self)
                return this._super();
            },
       cleanForSave: function() {
            this.$target.empty();
        },
    });
});




