odoo.define('pos_restaurant_ext_keyboard_app.pos', function(require){
	'use strict';

	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var popupwidget = require('point_of_sale.popups');
	var splitbill = require('pos_restaurant.splitbill');
	var printbill = require('pos_restaurant.printbill');

	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var field_utils = require('web.field_utils');
	var chrome = require('point_of_sale.chrome')
	var rpc = require('web.rpc');
	var session = require('web.session');
	var time = require('web.time');
	var utils = require('web.utils');
	var _t = core._t;
	
	var count = 0 ;
	var color = true;
	var config = false;
	var selected_partner = false;
	var screen =  false;
	var shop = 0;
	var widget_view = false;
	var want_invoice = false;
	var count_call = 0;


	gui.Gui.include({
		close_popup: function() {
        if  (this.current_popup) {
        	count = 0
            this.current_popup.close();
            this.current_popup.hide();
            this.current_popup = null;
        	}
    	},
	});

	chrome.OrderSelectorWidget.include({
		init: function(parent, options){
			var self = this;
			this._super(parent, options);
			$(document).on("keydown", function (e) {
					if(e.which== 45){
						if(screen == "product" && count == 0 && shop == 1){
							self.pos.add_new_order();
						}
					}
					if(e.which== 46){
						var order = self.pos.get_order(); 
						if(screen == "product" && count == 0 && shop == 1){
							if (!order) {
								return;
							} else if ( !order.is_empty() ){
								self.gui.show_popup('confirm',{
									'title': _t('Destroy Current Order ?'),
									'body': _t('You will lose any data associated with the current order'),
									confirm: function(){
										self.pos.delete_current_order();
									},
								});
							} else {
								self.pos.delete_current_order();
							}
						}
					}

			});
		}
	});

  screens.ProductScreenWidget.include({
	show: function(reset){
		this._super();
		screen = "product"
		if(this.pos.config.is_pos_restaurant_keyboard || this.pos.config.is_pos_shop_keyboard){
			shop = 1
		}
	}
  });


	screens.OrderWidget.include({	
		renderElement: function(){
			var self = this;
			this._super();
			$(document).on("keydown", function (e) {
				var order = self.pos.get_order();
				var mode = self.numpad_state.get('mode');

				var order  = self.pos.get_order();
				if (!order) {
					return;
				}
				var orderlines = order.get_orderlines();
				if(e.keyCode == 38){
				var s =0;
				if(screen == "product" && count == 0 && shop == 1){
					for(var  i = 0 ;i<orderlines.length ; i++){
						if(order.get_selected_orderline().cid == orderlines[i].cid ){
								s = i - 1
								if(s<=orderlines.length && s>=0){
									self.pos.get_order().select_orderline(orderlines[s]);
								}
								break;
							}
							
						}
					}
				
				}

				if(e.keyCode == 40 && count == 0 && shop == 1){
					if(screen == "product"){
						for(var  i = 0 ;i<orderlines.length ; i++){
							var s = i + 1
							if(order.get_selected_orderline()){
								if(order.get_selected_orderline().cid == orderlines[i].cid ){
									if(s< orderlines.length){
										self.pos.get_order().select_orderline(orderlines[s]);	
									}
									break;
								}						
							}
						}
					}
				}

				
			});
		}
	});

	screens.NumpadWidget.include({
		start: function(){
			var self = this;
			this._super();
			$(document).on("keydown", function (e) {
				if (e.which === 81 && count == 0 && shop == 1) {
					if(screen == "product"){
						self.state.changeMode('quantity');
					}
					
				}
				if (e.which === 68 && count == 0 && shop == 1) {
					if(screen == "product"){
						self.state.changeMode('discount');
					}
					
				}
				if (e.which === 80 && count == 0 && shop == 1) {
					if(screen == "product"){
						self.state.changeMode('price');
					}
					
				}
				/*
				if(e.which==8 && count == 0 && shop == 1){
					if(screen == "product"){
						self.state.deleteLastChar();
					}
					
				}
				if(e.which == 96){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(0);
					}
				}
			   if(e.which == 97){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(1);
					}
					
				}
				if(e.which == 98){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(2);
					}
					
				}
				if(e.which == 99){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(3);
					}
					
				}
				if(e.which == 100){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(4);
					}
					
				}
				if(e.which == 101){
					if(screen == "product" && shop == 1 ){
						self.state.appendNewChar(5);
					}
					
				}
				if(e.which == 102){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(6);
					}
					
				}
				if(e.which == 103){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(7);
					}
					
				}
				if(e.which == 104){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(8);
					}
					
				}
				if(e.which == 105){
					if(screen == "product" && shop == 1){
						self.state.appendNewChar(9);
					}
					
				}*/
			});
		}
		
	});
	
	screens.ActionpadWidget.include({
		renderElement: function(){
			var self = this;
			this._super();
			$(document).on("keydown", function (e) {
				if(e.ctrlKey && e.altKey && e.which == 68  && count == 0 && shop == 1){
					if(screen == "product"){
						count =1 
						self.gui.show_popup('number',{
							'title': _t('Discount Percentage'),
							'value': self.pos.config.discount_pc,
							'confirm': function(val) {
								val = Math.round(Math.max(0,Math.min(100,val)));
								self.apply_discount(val);
							},
						});
					}
				}
				if (e.which === 13 && count == 0 && shop == 1) {
					if(screen == "product"){
						 self.gui.show_screen('payment');
					}
					   
					}
				if (e.which === 67 && count == 0 && shop == 1) {
					if(screen == "product"){
						self.gui.show_screen('clientlist');
					}
					
				}
				if (e.which === 66 && count == 0 && shop == 1 && self.pos.config.is_pos_restaurant_keyboard && self.pos.config.iface_printbill) {
					if(screen == "product"){
						screen = "bill"
						self.gui.show_screen('bill');
					}
					
				}
				if (e.which === 83 && count == 0 && shop == 1 && self.pos.config.iface_splitbill && self.pos.config.is_pos_restaurant_keyboard) {
					if(screen == "product"){
						self.gui.show_screen('splitbill');
					}
					
				}
				
				if (e.which === 78 && count == 0 && shop == 1 && self.pos.config.iface_orderline_notes && self.pos.config.is_pos_restaurant_keyboard) {
					var line = self.pos.get_order().get_selected_orderline();
					if(screen == "product"){
						if (line) {
							count = 1
							self.gui.show_popup('textarea',{
								title: _t('Add Note'),
								value:   line.get_note(),
								confirm: function(note) {
									line.set_note(note);
								},
							});
						}
					}
				}
			    if (e.which === 84 && count == 0 && shop == 1 && self.pos.config.is_pos_restaurant_keyboard && self.pos.config.is_table_management) {
			    	if(screen == "product"){
				    	self.pos.transfer_order_to_different_table();
				    }
				}

				if (e.which === 71 && count == 0 && shop == 1 && self.pos.config.is_pos_restaurant_keyboard) {
					if(screen == "product"){
						count =1 
						self.gui.show_popup('number', {
							'title':  _t('Guests ?'),
							'cheap': true,
							'value':   self.pos.get_order().customer_count,
							'confirm': function(value) {
								value = Math.max(1,Number(value));
								self.pos.get_order().set_customer_count(value);
								self.renderElement();
							},
						});
					}
				}

			});
		}
		});

	screens.PaymentScreenWidget.include({
		show: function(){
		this._super();
		screen = "payment"
	},
		renderElement: function(){
			var self = this;
			this._super();
			$(document).on("keydown", function (e) {
				if (e.which === 67) {
					if(screen == "payment" && shop == 1){
					self.gui.show_screen('clientlist');	
					}
				}

				if(e.which==82){
					if(screen == "payment" && shop == 1){
						var order = self.pos.get_order();
					var lines = self.pos.get_order().get_paymentlines();
					for ( var i = 0; i < lines.length; i++ ) {
						if (lines[i].cid === order.selected_paymentline.cid) {
							self.pos.get_order().remove_paymentline(lines[i]);
							self.reset_input();
							self.render_paymentlines();
							// return;
						}
					}
					}
					
				}
				
				if (e.which === 84) {
					if(screen == "payment" && shop == 1  && self.pos.config.tip_product_id){

						self.click_tip();
					}
				}
				if (e.altKey &&e.which === 73) {
					if(screen == "payment" && shop == 1 && self.pos.config.module_account){
						var order = self.pos.get_order();
						order.set_to_invoice(true);
						self.$('.js_invoice').addClass('highlight');
					}
				}


				if (e.ctrlKey && e.which === 73) {
					if(screen == "payment" && shop == 1 && self.pos.config.module_account){
						var order = self.pos.get_order();
						order.set_to_invoice(false);
						self.$('.js_invoice').removeClass('highlight');
					}
				}

				if (e.which === 27) {
					if(screen == "payment" && shop == 1){

						self.gui.show_screen('products');
					}
					}

				
				if(e.keyCode == 38){
				var s =0;
				if(screen == 'payment' && shop == 1){
					var order  = self.pos.get_order();
					var paymentlines = order.get_paymentlines();
					for(var  i = 0 ;i<paymentlines.length ; i++){
					if(order.selected_paymentline.cid == paymentlines[i].cid ){
							s = i - 1
							if(s<=paymentlines.length && s>=0){
								order.select_paymentline(paymentlines[s]);
								self.render_paymentlines();
							}
							break;
						}
						
					}
				}
				
				}

				if(e.keyCode == 40){
					// var s =0;
					if(screen == "payment" && shop == 1){
						var order  = self.pos.get_order();
						var paymentlines = order.get_paymentlines();
						for(var  i = 0 ;i<paymentlines.length ; i++){
						var s = i + 1
						if(order.selected_paymentline){
							if(order.selected_paymentline.cid == paymentlines[i].cid ){
								if(s< paymentlines.length){
									order.select_paymentline(paymentlines[s]);
									self.render_paymentlines();
								}
								break;
							}						
						}
						}
					}
					
				}
		
			});
		}	
		});

	screens.ProductCategoriesWidget.include({
		renderElement: function(){
			var self = this;
			this._super();
			$(document).on("keydown", function (e) {
				if (e.which === 114 && shop == 1) {
					if(screen == "product" &&  shop == 1){
					count = 1;
					self.el.querySelector('.searchbox input').focus();
					self.el.querySelector('.searchbox input').value = "";
					e.preventDefault();

					}
				}

			if (e.which === 27) {
				if(screen == "product" && shop == 1){
					count = 0;
                    self.clear_search();
					self.el.querySelector('.searchbox input').blur();
					e.preventDefault();
					}
				}							
			});
		}
	});

	splitbill.SplitbillScreenWidget.include({
		show: function(){
		var self = this;
		this._super();
		this.renderElement();
		screen = "splitbill"
		var order = this.pos.get_order();
		var neworder = new models.Order({},{
			pos: this.pos,
			temporary: true,
		});
		neworder.set('client',order.get('client'));

		var splitlines = {};

		this.$('.orderlines').on('click','.orderline',function(){
			var id = parseInt($(this).data('id'));
			var $el = $(this);
			self.lineselect($el,order,neworder,splitlines,id);
		});

		this.$('.paymentmethods .button').click(function(){
			self.pay(order,neworder,splitlines);
		});
		$(document).on("keydown", function (e) {
			if(e.which== 80){
				if(screen == "splitbill" &&  shop == 1){
					self.pay(order,neworder,splitlines);
				}
			}
			if (e.which === 27) {
				if(screen == "splitbill" && shop == 1){

					self.gui.show_screen('products');
				}
			}
		});
		}
	});

	screens.ReceiptScreenWidget.include({
	show: function(){
		this._super();
		var self = this;
		screen = "receipt"
		var order = self.pos.get_order();
		$(document).on("keydown", function (e) {
			if(e.which == 80 && shop == 1){
				if(screen == "receipt"){
					self.print();
				}
			}
			if (e.which == 13 && shop == 1) {
				if(screen == "receipt"){
					order.finalize();
				}
			}
		});
	},
	});


	printbill.BillScreenWidget.include({
	show: function(){
		this._super();
		var self = this;
		screen = "printbill"
	},
	renderElement: function() {
		var self = this;
		this._super();
		$(document).on("keydown", function (e) {
			if(e.which == 80 && shop == 1){
				if(screen == "printbill"){
					self.print();
				}
			}
			if (e.which == 13 && shop == 1) {
				if(screen == "printbill"){
				self.click_next();
				}
			}

			if (e.which == 27 && shop == 1) {
				if(screen == "printbill"){
				self.click_back();
				}
			}
		});

		
	}
	});
	
	screens.ClientListScreenWidget.include({
		show: function(){
		var self = this;
		this._super();
		var flag =0;
		var editable = false;
		var search_editable = false;
		var edit_client = false;
		var add_client = false;
		screen = "client"
		 $(document).on("keydown", function (e) {
			if (e.which==114 && flag ==0 && shop == 1) {
				if(screen=="client"){
					if(search_editable == false){
					search_editable=true
					flag=1
					
					self.$('.searchbox input').focus();
					self.$('.searchbox input').val("");
					e.preventDefault();
				}
				}
				
			}
			if (e.which === 65 ) {
				if(screen == "client" && flag ==0  && shop == 1){
					if(add_client==false){
					add_client=true
					flag=1
					self.display_client_details('edit',{
						'country_id': self.pos.company.country_id,
					});
					self.$('.client-name').focus();
					self.$('.display_client_details.client-name').value = ""
					e.preventDefault();
				}
				}
				
			}

			if (e.which=== 69) {
				if(screen == "client" && flag ==0 && shop == 1){
					if(edit_client== false){
					edit_client=true
					flag=1
					self.edit_client_details(selected_partner);
					e.preventDefault();

				}
				}
				
				
			}


			if (e.which === 13 && flag ==1 && shop == 1) {
				if(screen == "client"){
					flag = 0
					if(edit_client==true){
					self.save_client_details(selected_partner);
				}
				if(add_client==true){
					// var self = this;
					// flag = 1
					flag = 0
					edit_client = true
					var fields = {};
					self.$('.client-details-contents .detail').each(function(idx,el){
						fields[el.name] = el.value || false;
					});

					if (!fields.name) {
						self.gui.show_popup('error',_t('A Customer Name Is Required'));
						return;
					}
					
					if (self.uploaded_picture) {
						fields.image = self.uploaded_picture;
					}

					fields.id           = selected_partner.id || false;
					fields.country_id   = fields.country_id || false;

					if (fields.property_product_pricelist) {
						fields.property_product_pricelist = parseInt(fields.property_product_pricelist, 10);
					} else {
						fields.property_product_pricelist = false;
					}
					var contents = self.$(".client-details-contents");
					contents.off("click", ".button.save");


					rpc.query({
							model: 'res.partner',
							method: 'create_from_ui',
							args: [fields],
						})
						.then(function(partner_id){
							self.saved_client_details(partner_id);
						},function(err,ev){
							ev.preventDefault();
							var error_body = _t('Your Internet connection is probably down.');
							if (err.data) {
								var except = err.data;
								error_body = except.arguments && except.arguments[0] || except.message || error_body;
							}
							self.gui.show_popup('error',{
								'title': _t('Error: Could not Save Changes'),
								'body': error_body,
							});
							self.save_client_details(selected_partner);
						});
				}
				if(self.old_client){
					self.$('.client-list .highlight').removeClass('highlight');
					var $button = self.$('.button.next');
					$button.toggleClass('oe_hidden',!self.has_client_changed());
					self.save_changes();
					self.gui.back();
				}
				}
				
				
		   
			}
			if (e.which === 27 && shop == 1) {
				if(screen == "client"){
					if(flag==1){
				self.$('.searchbox input').blur();
				self.$('.searchbox input')[0].value = ""
				self.clear_search()
				flag=0
				add_client = false
				editable = false
				search_editable=false
				edit_client=false
			  
			   }else{
				flag = 0
				add_client = false
				editable = false
				search_editable=false
				edit_client= false
				self.gui.show_screen('products');
			   }
			  	e.preventDefault();

				}
				
		   
		   }
			
		   

		   
	   });
	},
	line_select: function(event,$line,id){
		var partner = this.pos.db.get_partner_by_id(id);
		selected_partner = partner
		this.$('.client-list .lowlight').removeClass('lowlight');
		if ( $line.hasClass('highlight') ){
			$line.removeClass('highlight');
			$line.addClass('lowlight');
			this.display_client_details('hide',partner);
			this.new_client = null;
			this.toggle_save_button();
		}else{
			this.$('.client-list .highlight').removeClass('highlight');
			$line.addClass('highlight');
			var y = event.pageY - $line.parent().offset().top;
			this.display_client_details('show',partner,y);
			this.new_client = partner;
			this.toggle_save_button();
		}
	},
	});

});
