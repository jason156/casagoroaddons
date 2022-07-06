odoo.define('odoo_mo_top_vendors.top_vendor', function (require) {
    'use strict';
    var core = require('web.core');
    var QWeb = core.qweb;
    var AbstractAction = require('web.AbstractAction');
    var top_vendor_view = AbstractAction.extend({
        hasControlPanel: true,
        events: {
            'dblclick .categ': 'view_po',
        },


        init: function (parent, action) {
            $(".main_report").empty();
            this.report_name = action.report_name;
            this.lines = action.lines;
            return this._super.apply(this, arguments);

        },


        renderElement: function () {
            this._super();
            var self = this;
            var lines = [];
            if (this.lines) {
                for (var i in this.lines) {
                    lines.push(this.lines[i]);
                }
            }
            var $content = $(QWeb.render("report_top_vendor", {
                heading: self.report_name,
                id: self.id,
                type: 'report',
                lines: lines,
                group: this.group
            }));
            self.$el.html($content);
            return;
        },
        view_po: function (e) {
            var partner_id = $(e.target).data('id');
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: "purchase.order",
                name: "Top Vendors",
                domain: [['partner_id','=',partner_id],['state','=',"purchase"]],
                views: [[false, 'list']],
            });

        }

    });


    core.action_registry.add("top_vendor_view", top_vendor_view);
    return top_vendor_view;
});