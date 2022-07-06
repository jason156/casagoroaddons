odoo.define('pos_test_orders.pos_test_orders', function(require) {
            "use strict";
        var models = require('point_of_sale.models');
        var screens = require('point_of_sale.screens');
        var core = require('web.core');
        var mixins = require('web.mixins');
        var session = require('web.Session');
        var PosDB = require('point_of_sale.DB');
        var rpc = require('web.rpc');

        var posmodel_super = models.PosModel.prototype;
        models.PosModel = models.PosModel.extend({
        	push_order: function (order, opts) {
                opts = opts || {};
                var self = this;
                if (order != undefined && order.to_test){                	
                	self.pos_session.sequence_number--;
                	return true;
                }
                if (order) {
                    this.db.add_order(order.export_as_JSON());
                }
                return new Promise(function (resolve, reject) {
                    self.flush_mutex.exec(function () {
                        var flushed = self._flush_orders(self.db.get_orders(), opts);
                        flushed.then(resolve, reject);
                        return flushed;
                    });
                });
            },
//        	push_order: function(order, opts) {
//                opts = opts || {};
//                var self = this;
//                if (order != undefined && order.to_test){                	
//                	self.pos_session.sequence_number--;
//                	return true;
//                }
//                if(order){
//                    this.db.add_order(order.export_as_JSON());
//                }
//                var pushed = new $.Deferred();
//                this.flush_mutex.exec(function(){
//                    var flushed = self._flush_orders(self.db.get_orders(), opts);
//                    flushed.always(function(ids){
//                        pushed.resolve();
//                    });
//                    return flushed;
//                });
//                return pushed;
//            },
        });
        var _super_order = models.Order.prototype;
        models.Order = models.Order.extend({
        	initialize: function(attributes,options){
        		this.to_test = false;
        		_super_order.initialize.call(this,attributes,options);
        	},
        	set_to_test: function(to_test) {
                this.assert_editable();
                this.to_test = to_test;
            },
            is_to_test: function(){
                return this.to_test;
            },
            export_as_JSON: function() {
                var self = this;
                var json = _super_order.export_as_JSON.call(this);
                json.to_test = this.to_test;
                return json;
        	},
        });
        screens.PaymentScreenWidget.include({
        	click_test: function(){
                var order = this.pos.get_order();
                order.set_to_test(!order.is_to_test());
                if (order.is_to_test()) {
                    this.$('.js_test').addClass('highlight');
                } else {
                    this.$('.js_test').removeClass('highlight');
                }
            },
            renderElement: function() {
        		var self = this;
        		this._super();
        		this.$('.js_test').click(function(){
        			self.click_test();
        		});
        	},
        	finalize_validation: function() {
                var self = this;
                var order = this.pos.get_order();

                if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) { 

                        this.pos.proxy.open_cashbox();
                }

                order.initialize_validation_date();
                order.finalized = true;

                if (order.is_to_invoice()) {
                    var invoiced = this.pos.push_and_invoice_order(order);
                    this.invoicing = true;

                    invoiced.fail(this._handleFailedPushForInvoice.bind(this, order, false));

                    invoiced.done(function(){
                        self.invoicing = false;
                        self.gui.show_screen('receipt');
                    });
                } else {
                	debugger;
                    this.pos.push_order(order);
                    this.gui.show_screen('receipt');
                }

            },
        });
});
