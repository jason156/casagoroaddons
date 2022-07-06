odoo.define("pos_order_note.tour", function(require) {
    "use strict";

    var core = require("web.core");
    var tour = require("web_tour.tour");

    var _t = core._t;

    tour.register(
        "pos_order_note_tour",
        {
            url: "/web",
            test: true,
        },
        [
            tour.STEPS.SHOW_APPS_MENU_ITEM,
            {
                trigger: '.o_app[data-menu-xmlid="point_of_sale.menu_point_root"]',
                content: _t(
                    "Ready to launch your <b>point of sale</b>? <i>Click here</i>."
                ),
                position: "right",
                edition: "community",
            },
            {
                trigger: '.o_app[data-menu-xmlid="point_of_sale.menu_point_root"]',
                content: _t(
                    "Ready to launch your <b>point of sale</b>? <i>Click here</i>."
                ),
                position: "bottom",
                edition: "enterprise",
            },
            {
                trigger: ".o_pos_kanban button.oe_kanban_action_button",
                content: _t(
                    "<p>Click to start the point of sale interface. It <b>runs on tablets</b>, laptops, or industrial hardware.</p><p>Once the session launched, the system continues to run without an internet connection.</p>"
                ),
                position: "bottom",
            },
            {
                trigger: ".tables .table, .order-button.select-order.selected",
                content: _t("Click on table or make a dummy action"),
                position: "bottom",
                timeout: 30000,
            },
            {
                trigger: ".product-list .product",
                content: _t("<p>Select the first product in the product list</p>"),
                position: "bottom",
            },
            {
                trigger: ".control-button:has(.fa-tag)",
                content: _t("<p>Click on <b>Note</b> button</p>"),
                position: "bottom",
            },
            {
                trigger: ".product_note [data-id='1']",
                content: _t("<p>Click on the first predefined note</p>"),
                position: "bottom",
            },
            {
                trigger: ".product_note [data-id='2']",
                content: _t("<p>Click on the second predefined note</p>"),
                position: "bottom",
            },
            {
                trigger: ".popup-confirm-note .confirm",
                content: _t("<p>Click on Confirm button</p>"),
                position: "bottom",
            },
            {
                trigger: ".control-button:has(.fa-tag)",
                content: _t("<p>Click on <b>Note</b> button</p>"),
                position: "bottom",
            },
            {
                trigger: ".popup-confirm-note .order_type",
                content: _t("<p>Click on <b>Order Note</b></p>"),
                position: "bottom",
            },
            {
                trigger: ".product_note [data-id='3']",
                content: _t("<p>Click on predefined note</p>"),
                position: "bottom",
            },
            {
                trigger: ".popup-confirm-note .confirm",
                content: _t("<p>Click on Confirm button</p>"),
                position: "bottom",
            },
        ]
    );
});
