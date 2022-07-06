/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_invoice_details.pos_invoice_details', function(require) {
    "use strict";
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var pos_model = require('point_of_sale.models');
    var core = require('web.core');
    var QWeb = core.qweb;
    var SuperPosModel = pos_model.PosModel.prototype;


    pos_model.PosModel = pos_model.PosModel.extend({
        _save_to_server: function(orders, options) {
            var self = this;
            // POS Invoice Details - Dictionary and Loist Update--START--
            return SuperPosModel._save_to_server.call(this, orders, options).then(function(return_dict) {
                _.forEach(return_dict, function(dict){
                    if (dict.invoices != null) {
                        dict.invoices.forEach(function(invoice) {
                            self.db.pos_all_invoices.unshift(invoice);
                            self.db.invoice_by_id[invoice.id] = invoice;
                        });
                        dict.invoice_lines.forEach(function(invoice_line) {
                            self.db.pos_all_invoice_lines.unshift(invoice_line);
                            self.db.invoice_line_by_id[invoice_line.id] = invoice_line;
                        });
                    }
                    delete dict["invoices"];
                    delete dict["invoice_lines"];
                });
                // POS Invoice Details - Dictionary and Loist Update--STOP--
                return return_dict;
            });
        }
    });

    pos_model.load_models([{
        model: 'account.move',
        fields: ['invoice_user_id', 'id', 'name', 'state', 'partner_id', 'invoice_date', 'amount_total', 'amount_residual', 'invoice_line_ids'],
        domain: function(self) {
            return [
                ['state', '!=', 'draft']
            ]
        },
        loaded: function(self, invoices) {
            self.db.pos_all_invoices = invoices;
            self.db.invoice_by_id = [];
            invoices.forEach(function(invoice) {
                self.db.invoice_by_id[invoice.id] = invoice;
            });
        }
    }, {
        model: 'account.move.line',
        fields: ['id', 'product_id', 'name', 'account_id', 'quantity', 'price_unit', 'tax_ids', 'price_subtotal'],
        loaded: function(self, invoice_lines) {
            self.db.pos_all_invoice_lines = invoice_lines;
            self.db.invoice_line_by_id = [];
            invoice_lines.forEach(function(invoice_line) {
                self.db.invoice_line_by_id[invoice_line.id] = invoice_line;
            });
        }
    }]);

    screens.ClientListScreenWidget.include({

        display_client_details: function(visibility, partner, clickpos) {
            var self = this;
            self.pos.get_order().clientlist_previous_screen = this.pos.get_order().get_screen_data('previous-screen');
            self._super(visibility, partner, clickpos);
            self.$('.view_invoices').on('click', function(e) {
                self.click_view_invoices(partner);
            })
        },
        click_view_invoices: function(partner) {
            var self = this;
            var partner_id = partner.id;
            var invoices_for_customer = self.filter_invoices_by_customer(partner_id);
            self.gui.show_screen('wk_invoices', {
                'partner_id': partner_id,
                'invoices_for_customer': invoices_for_customer
            });

        },
        filter_invoices_by_customer: function(partner_id) {
            var self = this;
            var invoices_for_customer = [];
            self.pos.db.pos_all_invoices.forEach(function(invoice) {
                if (invoice.partner_id[0] == partner_id) {
                    invoices_for_customer.push(invoice);
                }
            });
            return invoices_for_customer;
        }
    });

    var InvoiceListScreenWidget = screens.ScreenWidget.extend({
        template: 'InvoiceListScreenWidget',

        get_invoices: function() {
            var self = this;
            if (self.gui) {
                return self.gui.get_current_screen_param('invoices_for_customer');
            } else
                return undefined;
        },
        display_invoices: function(intput_txt) {
            var self = this;
            var all_invoices_for_customer = this.get_invoices();
            var invoices_to_render = all_invoices_for_customer;

            if (intput_txt != undefined && intput_txt != '') {
                var new_invoice_data = [];
                var search_text = intput_txt.toLowerCase()
                all_invoices_for_customer.forEach(function(invoice) {
                    if( invoice.name && invoice.invoice_date && (((invoice.name.toLowerCase()).indexOf(search_text) != -1) || ((invoice.invoice_user_id[1].toLowerCase()).indexOf(search_text) != -1) ||
                        (invoice.invoice_date.toLowerCase()).indexOf(search_text) != -1)) {
                        new_invoice_data = new_invoice_data.concat(invoice);
                    }
                });
                invoices_to_render = new_invoice_data
            }

            var contents = this.$el[0].querySelector('.invoice-list-contents');
            contents.innerHTML = "";
            invoices_to_render.forEach(function(invoice) {
                var invoiceline_html = QWeb.render('WkInvoiceLine', {
                    widget: self,
                    invoice: invoice
                });
                var invoiceline = document.createElement('tbody');
                invoiceline.innerHTML = invoiceline_html;
                invoiceline = invoiceline.childNodes[1];
                contents.appendChild(invoiceline);
            });
        },
        show: function() {
            var self = this;
            this._super();
            this.renderElement();
            this.details_visible = false;
            this.display_invoices(undefined);
            this.$('.invoice_search').keyup(function() {
                self.display_invoices(this.value);
            });
            this.$('.back').click(function() {
                self.gui.show_screen(self.pos.get_order().clientlist_previous_screen);
            });
            this.$('.invoice-list-contents').delegate('.invoice-line', 'click', function(event) {
                self.line_select(event, $(this), parseInt($(this).data('id')));
            });
            var contents = this.$('.invoice-details-contents');
            contents.empty();
            var parent = self.$('.wk_invoice_table').parent();
            parent.scrollTop(0);
        },
        line_select: function(event, $line, id) {
            var self = this;
            var invoice = self.pos.db.invoice_by_id[id];
            if ($line.hasClass('wk_highlight')) {
                self.$('.wk_invoice_table .wk_highlight').removeClass('wk_highlight');
                $(".invoice-line").css("background-color", "");
                self.display_invoice_details('hide', null);
            } else {
                self.$('.wk_invoice_table .wk_highlight').removeClass('wk_highlight');
                $(".invoice-line").css("background-color", "");
                $line.addClass('wk_highlight');
                $line.css("background-color", "rgb(110,200,155) !important");
                var y = event.pageY - $line.parent().offset().top;
                self.display_invoice_details('show', invoice, y);
            }
        },
        display_invoice_details: function(visibility, invoice, clickpos) {
            var self = this;
            var contents = this.$('.invoice-details-contents');
            var parent = this.$('.wk_invoice_table').parent();
            var scroll = parent.scrollTop();
            var height = contents.height();
            var invoicelines = [];
            if (visibility == 'show') {
                invoice.invoice_line_ids.forEach(function(line_id) {
                    invoicelines.push(self.pos.db.invoice_line_by_id[line_id]);
                });
                contents.empty();
                contents.append($(QWeb.render('InvoiceDetails', { widget: self, invoice: invoice, invoicelines: invoicelines })));
                var new_height = contents.height();
                if (!this.details_visible) {
                    if (clickpos < scroll + new_height + 20) {
                        parent.scrollTop(clickpos - 20);
                    } else {
                        parent.scrollTop(parent.scrollTop() + new_height);
                    }
                } else {
                    parent.scrollTop(parent.scrollTop() - height + new_height);
                }
                self.$("#close_invoice_details").on("click", function() {
                    self.$('.wk_invoice_table .wk_highlight').removeClass('wk_highlight');
                    $(".invoice-line").css("background-color", "");
                    self.display_invoice_details('hide', null);
                });
                this.details_visible = true;
            }
            if (visibility == 'hide') {
                contents.empty();
                if (height > scroll) {
                    contents.css({ height: height + 'px' });
                    contents.animate({ height: 0 }, 400, function() {
                        contents.css({ height: '' });
                    });
                } else {
                    parent.scrollTop(parent.scrollTop() - height);
                }
                this.details_visible = false;
                $('.wk_invoice_table .wk_highlight').removeClass('wk_highlight');
                $(".invoice-line").css("background-color", "");
            }
        },
    });
    gui.define_screen({ name: 'wk_invoices', widget: InvoiceListScreenWidget });

    return {
        InvoiceListScreenWidget: InvoiceListScreenWidget
    }
});