odoo.define('cft_product_variant_mapping.variant_mapping_screen', function (require) {
'use strict';

var core = require('web.core');
var Widget = require('web.Widget');
var AbstractAction = require('web.AbstractAction');
var _t = core._t;

var variant_mapping_screen = AbstractAction.extend({
    events:{
        'click .add_product': 'add_product',
        'click .close_template': 'close_template',
    },
    
    init: function(parent, action) {
        this.actionManager = parent;
        this.action = action;
        this.domain = [];
        this.template_id = action.res_id;
        var self = this;
        return this._super.apply(this, arguments);
    },
    
    willStart: function() {
        return this.get_html();
    },
    start: function() {
        var self = this;
        this.update_cp();
        return this._super.apply(this, arguments).then(function () {
            self.$el.html(self.html);
        });
    },
    
    close_template: function(e) {
    	e.preventDefault();
        e.target.parentElement.parentElement.parentElement.parentElement.parentElement.remove();        
    },
    
    // Updates the control panel and render the elements that have yet to be rendered
    update_cp: function() {
        var status = {
        	clear_breadcrumbs: false
        }
        return this.updateControlPanel(status);
    },
    
    add_product: function(e) {
    	e.preventDefault();
        var self = this;
        var template_id = $( "#sel1" ).val();
        var execute = true;
        $(".main-template").each(function(){
           if($(this).getAttributes().id == template_id){
               alert("This template is already selected.");
               execute = false;
           }
    	});
    	
    	if(execute){
    		return this._rpc({
                model: 'product.template',
                method: 'add_product',
                args: [template_id],
            })
            .then(function (result) {
            	$("#template_grid").append(result.html);
            });
            
    	}else{
    	  return
    	}
        
    },

    
    
    // Fetches the html and is previous report.context if any, else create it
    get_html: function() {
        var self = this;
        return this._rpc({
                model: 'product.template',
                method: 'get_html',
                args: [self.template_id],
            })
            .then(function (result) {
                self.html = result.html;
                self.report_context = result.report_context;
            });
    },

    

});

core.action_registry.add("variant_rearrange_screen", variant_mapping_screen);
return variant_mapping_screen;
});
