/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_barcode_screen.pos_barcode_screen', function(require) {
	"use strict";
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var chrome = require('point_of_sale.chrome');
	var PosBaseWidget = require('point_of_sale.BaseWidget');	
	var SuperProductScreen = screens.ProductScreenWidget.prototype;
	var SuperOrder = models.Order.prototype;
	var core = require('web.core');	
	var QWeb = core.qweb;	

	screens.ProductScreenWidget.include({
		
		events : _.extend({}, SuperProductScreen.events, {
			'click .pad_tg': 'toggle_pads',

			'click .wk_searchbox':'click_search_handler'
		}),

		click_search_handler: function(event){
			if(event)
			$('.product-screen .rightpane').show();
			$('.wk_barcode_screen').hide();
			$('.order-scroller.touch-scrollable').show();
			$('.wk_image_box').hide();
			$('.product-screen .searchbox input').focus()
		},
		
        toggle_pads:function(){  
            var self = this;
            self.$('.pad_tg').parent().siblings('div').slideToggle();
        },
		show: function(reset){
			var self = this;
			self._super(reset);
			self.display_orderline();
			if(self.pos.show_barcode_screen){
				$('.product-screen .rightpane').hide();
				$('.wk_barcode_screen').show()
			}
			else{
				$('.product-screen .rightpane').show();
				$('.wk_barcode_screen').hide();
			}
			self.$('.wk-order-list-contents').delegate('.wk-order-line', 'click', function(event) {
                event.stopImmediatePropagation();
				self.line_select($(this), parseInt($(this).data('id')));
            });

		},
		line_select: function($line, id) {
            var self = this;
			var order = self.pos.get_order();
			var orderline = (order && id) ? order.get_orderline(id) : false;
			if(id && order && orderline){
				$('.wk-order-line.wk_highlight').removeClass('wk_highlight');
				$line.addClass('wk_highlight');
				self.order_widget.numpad_state.reset();
				order.select_orderline(orderline);
			}
        },
		display_orderline: function() {
			var self = this;
			var order = self.pos.get_order();

			var contents = this.$el[0].querySelector('.wk-order-list-contents');
			contents.innerHTML = "";			
			var wk_orderline_list = order.get_orderlines();
			wk_orderline_list.forEach(function(orderline){			
				var orderline_html = QWeb.render('Wk-OrderLine', {
					widget: self,
					wk_orderline: orderline
				});
				var wk_orderline = document.createElement('tbody');
				wk_orderline.innerHTML = orderline_html;
				wk_orderline = wk_orderline.childNodes[1];
				orderline.wk_node = wk_orderline;
				var el_lot_icon = wk_orderline.querySelector('.line-lot-icon');
				if(el_lot_icon){
					el_lot_icon.addEventListener('click', (function() {
						self.order_widget.show_product_lot(orderline);
					}.bind(this)));
				}
				if(orderline.selected){
					$('.wk-order-line.wk_highlight').removeClass('wk_highlight');
					$(wk_orderline).addClass('wk_highlight');	
				}
				contents.appendChild(wk_orderline);
			});
			if(self.pos.show_barcode_screen){
				$('.wk_image_box').show();
				$('.order-scroller.touch-scrollable').hide();
				if(order.selected_orderline && order.selected_orderline.product){
					let product = order.selected_orderline.product;
					$(".wk_cart_product").attr("src",self.order_widget.get_selected_line_product_url(product));
					$(".wk_selected_product_name").text(product.display_name);
					if(product.description_sale){
						$(".wk_product_description").show();
						$(".wk_product_description .product_desc").text(product.description_sale);
					}
					else
						$(".wk_product_description").hide();
				}
			}
			else{
				$('.order-scroller.touch-scrollable').show();
				$('.wk_image_box').hide();
			}
		},
	});

	screens.OrderWidget.include({
		
		renderElement: function(scrollbottom){
			var self = this;
			self._super(scrollbottom);
			if(self.pos && self.pos.show_barcode_screen){
				$(this.el.querySelector('.order-scroller')).hide();
				$(this.el.querySelector('.wk_image_box')).show();
				if(self.pos.chrome &&self.pos.chrome.screens && self.pos.chrome.screens.products){
					self.pos.chrome.screens.products.display_orderline()
				}
				$('.wk_image_box').show();
				$('.order-scroller.touch-scrollable').hide();
			}
			else{
				$(this.el.querySelector('.order-scroller')).show()
				$(this.el.querySelector('.wk_image_box')).hide()
			}
			
		},
		wk_render_orderline: function(orderline){
			var contents = this.$el[0].querySelector('.wk-order-list-contents');
			var wk_orderline_html = QWeb.render('Wk-OrderLine', {
				widget: this,
				wk_orderline: orderline
			});
			var wk_orderline = document.createElement('tbody');
			wk_orderline.innerHTML = wk_orderline_html;
			wk_orderline = wk_orderline.childNodes[1];
			orderline.wk_node = wk_orderline;
			var el_lot_icon = wk_orderline.querySelector('.line-lot-icon');
			if(el_lot_icon){
				el_lot_icon.addEventListener('click', (function() {
					this.show_product_lot(orderline);
				}.bind(this)));
			}
			return wk_orderline;
        },

		wk_remove_orderline: function(wk_node){
			var self = this;
			if(wk_node.parentNode){
            	wk_node.parentNode.removeChild(wk_node);
				var order = self.pos.get_order()
				if (order){
					$('.wk_orderline_list_table').scrollTop(100*order.get_orderlines().length)
				}
			}
        },

		rerender_orderline: function(order_line){
			var self = this;
			self._super(order_line);
			if(order_line.wk_node){
				var wk_node = order_line.wk_node;
				var wk_replacement_line = this.wk_render_orderline(order_line);
				if(wk_node.parentNode){
					wk_node.parentNode.replaceChild(wk_replacement_line,wk_node);
					$('.wk-order-line.wk_highlight').removeClass('wk_highlight');
					$(wk_replacement_line).addClass('wk_highlight');
				}
				
			}
			else if(self.pos.pos_widget && self.pos.pos_widget.screen_selector && self.pos.pos_widget.screen_selector.screen_set.wkitemlist){
				self.pos.pos_widget.screen_selector.screen_set.wkitemlist.display_orderline();
			}
			if(self.pos.show_barcode_screen){
				let product = order_line.product;
				$('.wk_image_box').show();
				$('.order-scroller.touch-scrollable').hide();
				$(".wk_cart_product").attr("src",self.get_selected_line_product_url(product));
				$(".wk_selected_product_name").text(product.display_name);
				if(product.description_sale){
					$(".wk_product_description").show();
					$(".wk_product_description .product_desc").text(product.description_sale);
				}
				else
					$(".wk_product_description").hide();
			}
			else{
				$('.order-scroller.touch-scrollable').show();
				$('.wk_image_box').hide();
			}
		},

		remove_orderline: function(order_line){
            var self = this;
			self._super(order_line)
			if(order_line && order_line.wk_node)
				self.wk_remove_orderline(order_line.wk_node)
			if(self.pos.get_order() && self.pos.get_order().get_orderlines().length == 0){
				$('.order-scroller.touch-scrollable').hide();
			}
        },

		get_selected_line_product_url: function(product){
			var self = this;
			var order = self.pos.get_order();
			if(product)
				return window.location.origin + '/web/image?model=product.product&field=image_128&id='+product.id;
			else if(order && order.select_orderline && order.select_orderline.product)
				return window.location.origin + '/web/image?model=product.product&field=image_128&id='+order.select_orderline.product.id;
			else
				return;
		},

		update_summary: function(){
			var self = this;
			self._super();
			var order = this.pos.get_order();
			var total     = order ? order.get_total_with_tax() : 0;
			var taxes     = order ? total - order.get_total_without_tax() : 0;
            $('.wk_summary .wk_entry .wk_total').text(self.format_currency(total));
            $('.wk_summary .wk_entry .subentry.value').text(self.format_currency(taxes));
        },
	});

	var WkBarcodeWidget = PosBaseWidget.extend({
		template: 'WkBarcodeWidget',
		
		init: function(parent, options) {
			this._super(parent, options);
			this.pos.show_barcode_screen = true;
		},

		start: function(){
			var self = this;
			self._super();
			this.$el.on("click",function(event){
				if(self.pos.show_barcode_screen)
					self.$('.wk_barcode_screen_status').removeClass('oe_green');
				else
					self.$('.wk_barcode_screen_status').addClass('oe_green');
				self.pos.show_barcode_screen = !self.pos.show_barcode_screen;
				if(self.gui && self.gui.current_screen)
					self.gui.current_screen.show()		
			});
			

		}
	});
	chrome.Chrome.prototype.widgets.unshift({
		'name':   'multi_printer',
		'widget': WkBarcodeWidget,
		'append':  '.pos-rightheader',
		'condition': function(){ return this.pos.config.show_barcode_screen},
	});
	
	models.Order = models.Order.extend({
		add_product: function(product, options){
			var self = this;
			SuperOrder.add_product.call(self,product,options);
			if(self.pos.show_barcode_screen && !$('.wk_barcode_screen').is(":visible")){
				self.pos.gui.current_screen.show();
			}
			if(self.pos.show_barcode_screen){
				if (self){
					$('.wk_orderline_list_table').scrollTop(100*self.get_orderlines().length)
				}
			}
		}
	})
});
