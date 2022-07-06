/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_register_invoice_payments.pos_register_invoice_payments', function(require) {
    "use strict";
    var screens = require('point_of_sale.screens');
    var popups = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var pos_model = require('point_of_sale.models');
    var core = require('web.core');
    var rpc = require('web.rpc')
    var QWeb = core.qweb;
    var inv_details_screen = require('pos_invoice_details.pos_invoice_details')

    var RegisterPaymentPopup = popups.extend({
        template: 'RegisterPaymentPopup',
        events: {
            'click .cancel_credit_line': 'click_cancel',
            'click .button.register_payment': 'wk_register_payment',
            'click .tab-link': 'wk_change_tab',
            'click .outstanding_credit_line': 'wk_use_outstanding_credit',
            'click .reconsile_line': 'remove_move_reconcile',
        },
        wk_register_payment: function(event) {
            var self = this;
            var invoice = self.options.invoice;
            var amount = parseFloat(self.$('.payment_amount').val());
            var payment_memo = self.$('.payment_memo').val();
            var wk_payment_journal = parseInt(self.$('.wk_payment_journal').val());

            var wk_register = _.find(self.pos.payment_methods, function(method) { return method.id == wk_payment_journal; });

            if (amount <= 0 || !amount) {
                self.$('.payment_amount').removeClass('text_shake');
                self.$('.payment_amount').focus();
                self.$('.payment_amount').addClass('text_shake');
                return;
            } else if (self.$('.wk_payment_journal').val() == "") {
                self.$('.wk_payment_journal').removeClass('text_shake');
                self.$('.wk_payment_journal').focus();
                self.$('.wk_payment_journal').addClass('text_shake');
                return;
            } else {
                $('.button.register_payment').css('pointer-events', 'none')
                rpc.query({
                        model: 'account.move',
                        method: 'wk_register_invoice_payment',
                        args: [{
                            'amount': amount,
                            'payment_memo': payment_memo,
                            'payment_method_id': wk_payment_journal,
                            'invoice_id': invoice.id,
                            'journal_id': wk_payment_journal,
                            'statement_id': wk_register.id,
                            'pos_order_id':self.pos.get_order().id,
                            'session_id': self.pos.pos_session.id,
                        }]
                    })
                    .then(function(result) {
                        if (result && result.residual >= 0) {
                            invoice.amount_residual = parseFloat(result.residual);
                            if (result.state)
                                invoice.state = result.state;
                            self.pos.gui.close_popup();
                            self.update_residual_amount(invoice.amount_residual);
                        };
                        $('.button.register_payment').css('pointer-events', '')
                    })
                    .catch(function(unused, event) {
                        self.gui.show_popup('error', {
                            title: 'Failed To Register Payment.',
                            body: 'Please make sure you are connected to the network.',
                        });
                        $('.button.register_payment').css('pointer-events', '')
                    });
            }

        },
        update_residual_amount: function(amount) {
            var self = this;
            var invoice = self.options.invoice;
            self.$('.wk_residual_amount.text_shake').removeClass('text_shake');
            self.$('.wk_residual_amount').addClass('text_shake');
            self.$('.wk_residual_amount').text('Amount Due : ' + self.format_currency(amount));
            $('.wk_invoice_state h2').text(invoice.state[0].toUpperCase() + invoice.state.slice(1));
            $('.invoice-line.wk_highlight td:last-child').text(self.format_currency(amount));
            $('.selected_line_residual_amount').text(self.format_currency(amount));
        },
        wk_use_outstanding_credit: function(event) {
            var self = this;
            var wk_id = $(event.target).length ? $(event.target)[0].id : false;
            self.$('.outstanding_credit_line').css('pointer-events', 'none')
            $(event.target).css("background", "#e3f6ed")
            $(event.target).closest('tr').css("background", "#e3f6ed");
            var invoice = self.options.invoice;
            if (wk_id && invoice) {
                rpc.query({
                        model: 'account.move',
                        method: 'wk_assign_outstanding_credit',
                        args: [invoice.id, parseInt(wk_id)],
                    }).then(function(result) {
                        if (result) {
                            var outstanding_credits;
                            var payments_widget;
                            var invoice = self.options.invoice;
                            if (result && result.length && invoice) {
                                invoice.amount_total = result[0].amount_total;
                                invoice.amount_residual = result[0].amount_residual;
                                outstanding_credits = JSON.parse(result[0].invoice_outstanding_credits_debits_widget);
                                payments_widget = JSON.parse(result[0].invoice_payments_widget);
                                invoice.state = result[0].state;
                            }
                            var data = {
                                outstanding_credits: outstanding_credits,
                                payments_widget: payments_widget,
                                invoice: invoice
                            };
                            self.update_residual_amount(invoice.amount_residual);
                            self.render_invoice_payment_lines(data);
                        }
                        self.$('.outstanding_credit_line').css('pointer-events', '')
                    })
                    .catch(function(unused, event) {
                        self.gui.show_popup('error', {
                            title: 'Failed To Register Payment.',
                            body: 'Please make sure you are connected to the network.',
                        });
                        self.$('.outstanding_credit_line').css('pointer-events', '')
                    });
            }
        },
        wk_rerender_lines: function(invoice_id) {
            var self = this;
            var invoice_id = parseInt(invoice_id);
            rpc.query({
                    model: 'account.move',
                    method: 'read',
                    args: [
                        [invoice_id],
                    ],
                })
                .then(function(result) {
                    var outstanding_credits;
                    var payments_widget;
                    var invoice = self.options.invoice;
                    if (result && result.length && invoice) {
                        invoice.amount_total = result[0].amount_total;
                        invoice.amount_residual = result[0].amount_residual;
                        outstanding_credits = JSON.parse(result[0].invoice_outstanding_credits_debits_widget);
                        payments_widget = JSON.parse(result[0].invoice_payments_widget);
                        invoice.state = result[0].state;
                    }
                    var data = {
                        outstanding_credits: outstanding_credits,
                        payments_widget: payments_widget,
                        invoice: invoice
                    };
                    self.update_residual_amount(invoice.amount_residual);
                    self.render_invoice_payment_lines(data);

                })
                .catch(function(unused, event) {
                    console.log("dsafasdf123eqw33asd")
                    self.gui.show_popup('error', {
                        title: 'Failed To  Rerender Lines.',
                        body: 'Please make sure you are connected to the network.',
                    });
                });

        },
        remove_move_reconcile: function(event) {
            var self = this;
            var paymentId = $(event.target).length ? $(event.target)[0].id : false;
            var invoice_id = self.options.invoice ? self.options.invoice.id : false;
            self.$('.reconsile_line').css('pointer-events', 'none');
            $(event.target).css("background", "#db8b8b")
            $(event.target).closest('tr').css("background", "#db8b8b")
            if (paymentId && invoice_id) {
                rpc.query({
                        model: 'account.move.line',
                        method: 'remove_move_reconcile',
                        args: [parseInt(paymentId)]
                    }).then(function() {
                        self.wk_rerender_lines(invoice_id);
                        self.$('.reconsile_line').css('pointer-events', '');
                    })
                    .catch(function(unused, event) {
                        self.gui.show_popup('error', {
                            title: 'Failed To  Rerender Lines.',
                            body: 'Please make sure you are connected to the network.',
                        });
                        self.$('.reconsile_line').css('pointer-events', '');
                    });
            }
        },
        wk_change_tab: function(event) {
            var target_tab_id = $(event.target)[0].id;
            if (target_tab_id) {
                this.$('.tab-content').removeClass('current');
                this.$('.tab-link').removeClass('current');
                $(event.currentTarget).addClass('current');
                this.$(target_tab_id).addClass('current');
                if (target_tab_id == '#register_payment_tab')
                    $('.button.register_payment').show();
                else
                    $('.button.register_payment').hide();
            }
        },
        render_invoice_payment_lines: function(data) {
            var self = this;
            var payments_widget_lines = data.payments_widget ? data.payments_widget.content : [];
            var credit_lines = data.outstanding_credits ? data.outstanding_credits.content : [];
            var invoice = data.invoice

            var contents = this.$el[0].querySelector('.payment-widget-list-contents');
            contents.innerHTML = "";
            payments_widget_lines.forEach(function(content) {
                var paymentline_html = QWeb.render('WkPaymentWidgetline', {
                    widget: self,
                    content: content
                });
                var paymentline = document.createElement('tbody');
                paymentline.innerHTML = paymentline_html;
                paymentline = paymentline.childNodes[1];
                contents.appendChild(paymentline);
            });
            var creditcontents = this.$el[0].querySelector('.outstanding-credit-list-contents');
            creditcontents.innerHTML = "";
            credit_lines.forEach(function(content) {
                var credit_line_html = QWeb.render('WkOutstandingCreditline', {
                    widget: self,
                    content: content
                });
                var credit_lines = document.createElement('tbody');
                credit_lines.innerHTML = credit_line_html;
                credit_lines = credit_lines.childNodes[1];
                creditcontents.appendChild(credit_lines);
            });
            if (!payments_widget_lines.length) {
                $('.tab-link.reconsile').removeClass('current');
                $('.tab-link.reconsile').hide();
                $('#reconsile_tab').removeClass('current');
                $('.tab-link.outstanding_credits').click();
            } else {
                $('.tab-link.reconsile').show();
            }
            if (!credit_lines.length) {
                $('.tab-link.outstanding_credits').removeClass('current');
                $('.tab-link.outstanding_credits').hide();
                $('#outstanding_credits_tab').removeClass('current');
                $('.tab-link.reconsile').click();
            } else {
                $('.tab-link.outstanding_credits').show();
            }
            if (invoice.amount_residual) {
                $('.tab-link.manual_payment').show();
                if (!(payments_widget_lines.length || credit_lines.length))
                    $('.tab-link.manual_payment').click();
            } else {
                $('.tab-link.manual_payment ').hide();
                $('#register_payment_tab').removeClass('current');
            }
        },
        show: function(options) {
            var self = this;
            self.options = options || {};
            self._super(self.options);
            self.options = options || {};
            self.render_invoice_payment_lines(options);
            if ($('.tab-link').length) {
                $('.tab-link').removeClass('current');
                if (options.payments_widget) {
                    $($('.tab-link')[0]).click();
                } else if (options.outstanding_credits) {
                    $($('.tab-link')[1]).click();
                }
            }
        },
    });
    gui.define_popup({ name: 'register_payment', widget: RegisterPaymentPopup });

    inv_details_screen.InvoiceListScreenWidget.include({
        display_invoice_details: function(visibility, invoice, clickpos) {
            var self = this;
            self._super(visibility, invoice, clickpos);
            self.$('.wk_register_payment').on('click', function(e) {
                rpc.query({
                        model: 'account.move',
                        method: 'read',
                        args: [
                            [invoice.id],
                            ['invoice_outstanding_credits_debits_widget', 'invoice_payments_widget', 'state', 'amount_total', 'amount_residual']
                        ],
                    })
                    .then(function(result) {
                        console.log("Result", result)
                        var outstanding_credits;
                        var payments_widget;
                        console.log("payment1")
                        console.log("json", JSON.parse(result[0].invoice_outstanding_credits_debits_widget))
                        console.log("payment2");
                        if (result && result.length) {
                            invoice.amount_total = result[0].amount_total;
                            invoice.amount_residual = result[0].amount_residual;
                            outstanding_credits = JSON.parse(result[0].invoice_outstanding_credits_debits_widget);
                            payments_widget = JSON.parse(result[0].invoice_payments_widget);
                        }
                        console.log(payments_widget, "invoice", invoice)
                        self.pos.gui.show_popup('register_payment', {
                            outstanding_credits: outstanding_credits,
                            payments_widget: payments_widget,
                            invoice: invoice
                        });
                    })
                    // .catch(function(unused, event) {
                    //     console.log("dsafa5as46d56f4s56d4f65s4df56sdfasd")
                    //     self.gui.show_popup('error', {
                    //         title: 'Failed To Register Payment.',
                    //         body: 'Please make sure you are connected to the network.',
                    //     });
                    // });
            });
        }
    })
});