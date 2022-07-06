odoo.define('pos_operation_restrict.pos_operation', function (require) {
"use strict";

    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var PopupWidget = require('point_of_sale.popups');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var _t = core._t;

    models.load_fields("res.users", ['partner_id','based_on','can_give_discount','can_change_price', 'discount_limit']);

    var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        set_cashier: function(employee){
            var self = this;
            posmodel_super.set_cashier.apply(this, arguments);
            if(self.user){
                var current_user = self.user;
                employee['based_on'] = current_user['based_on'];
                employee['can_give_discount'] = current_user['can_give_discount'];
                employee['can_change_price'] = current_user['can_change_price'];
                employee['discount_limit'] = current_user['discount_limit'];
                employee['partner_id'] = current_user['partner_id'];
            }
            this.set('cashier', employee);
            this.db.set_cashier(this.get('cashier'));
        },
    });

    gui.Gui.include({
        authentication_pin: function(password) {
            var self = this;
            var ret = new $.Deferred();
            var flag = false;
            self.show_popup('password',{
                'title': _t('Password ?'),
                confirm: function(pw) {
                    _.each(password, function(pass) {
                        if (pw === pass) {
                            flag = true;
                        }
                    });
                    if(flag){
                        ret.resolve();
                    } else {
                        self.show_popup('error',_t('Incorrect Password'));
                        ret.reject()
                    }
                },
            });
            return ret;
        },
    });

	screens.OrderWidget.include({
		set_value: function(val) {
		    var self = this;
	    	var order = this.pos.get_order();
	    	if(this.pos.config.enable_operation_restrict){
		    	if (order.get_selected_orderline()) {
		            var mode = this.numpad_state.get('mode');
		            var cashier = this.pos.get_cashier() || false;
		            if( mode === 'quantity'){
		                order.get_selected_orderline().set_quantity(val);
		            }else if( mode === 'discount'){
		            	if(cashier && cashier.can_give_discount){
		            		if(val <= cashier.discount_limit || cashier.discount_limit < 1){
		            			order.get_selected_orderline().set_discount(val);
		            			if(val == ''){
		            				this.numpad_state.change_mode = true
		            			}
		            		} else {
		            		    if(cashier.based_on == 'barcode'){
		            			    this.gui.show_popup('ManagerAuthenticationPopup', { val: val });
		            			}
		            			else{
		            			    var password = [];
		            			    var GetEmployeePin = new Promise(function(resolve, reject){
                                        rpc.query({
                                            model: 'hr.employee',
                                            method: 'get_user_pin',
                                            args: [self.pos.config.pos_managers_ids],
                                        })
                                        .then(function(employees) {
                                            if(employees){
                                                resolve(employees);
                                            }else{
                                                reject();
                                            }
                                        });
                                    })
                                    GetEmployeePin.then(function(employees){
                                        if(employees){
                                            if(employees && employees.length > 0){
                                                _.each(employees, function(each_emp){
                                                    password.push(each_emp.pin)
                                                });
                                            }
                                            if(password && password.length > 0){
                                                var res = self.gui.authentication_pin(password).then(function(){
                                                    self.pos.get_order().get_selected_orderline().set_discount(val);
                                                    self.gui.close_popup();
                                                });
                                            }
                                        }
                                    })
		            			}
		            		}
		            	} else {
		            		alert(_t('You don\'t have access to give discount.'));
		            	}
		            }else if( mode === 'price'){
		            	if(cashier && cashier.can_change_price){
		            		order.get_selected_orderline().set_unit_price(val);
		            	} else {
		            		alert(_t('You don\'t have access to change Price.'));
		            	}
		            }
		    	}
	    	} else {
	    		this._super(val)
	    	}
	    },
	});

	var ManagerAuthenticationPopup = PopupWidget.extend({
	    template: 'ManagerAuthenticationPopup',
	    show: function(options){
	    	var self = this;
	    	this.value = options.val || 0;
	    	options = options || {};
	        this._super(options);
	        this.renderElement();
	        $('#manager_barcode').focus();
	        $('#manager_barcode').keypress(function(e){
	        	if(e.which === 13){
	        		self.click_confirm();
	        	}
	        });
	    },
	    click_confirm: function(){
	    	var self = this;
	    	var barcode_input = $('#manager_barcode').val();
	    	if(barcode_input){
		    	if(!$.isEmptyObject(self.pos.config.pos_managers_ids)){
		    	    var users_list = [];
                    _.each(self.pos.users, function(user){
                        self.pos.config.pos_managers_ids.map(function(user_id){
                            if(user_id == user.id){
                                if(user.partner_id && user.partner_id[0]){
                                    var related_partner = self.pos.db.partner_by_id[user.partner_id[0]];
                                    if(related_partner){
                                        user['barcode'] = related_partner.barcode;
                                        users_list.push(user);
                                    }
                                }
                            }
                        })
                    });
                    if(users_list && users_list.length > 0){
                        var result_find = _.find(users_list, function (o) {
                            return o.barcode === barcode_input;
                        });    
                    }
		    		if(result_find && !$.isEmptyObject(result_find)){
		    			if($.inArray(result_find.id, self.pos.config.pos_managers_ids) != -1){
		    				if(result_find.can_give_discount){
		    				    self.pos.get_order().get_selected_orderline().set_discount(self.value);
		    				    self.gui.close_popup();
		    				} else {
		    					alert(_t(result_find.name + ' does not have right to give discount.'));
	    				}
		    			} else {
		    				alert(_t('Not a Manager.'));
			    		}
		    		} else {
		    			alert(_t('No result found'));
		    			$('#manager_barcode').val('');
		    			$('#manager_barcode').focus();
		    		}
		    	}
	    	}else{
	    		alert(_t('Please enter barcode.'));
	    		$('#manager_barcode').focus();
	    	}
	    },
	});
	gui.define_popup({name:'ManagerAuthenticationPopup', widget: ManagerAuthenticationPopup});
});
