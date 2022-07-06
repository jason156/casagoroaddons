odoo.define("pos_container.pos", function (require) {
  "use strict";

  var gui = require("point_of_sale.gui");
  var models = require("point_of_sale.models");
  var PopupWidget = require("point_of_sale.popups");
  var screens = require("point_of_sale.screens");

  models.load_fields("product.product", [
    "is_pack",
    "packed_product_ids",
    "weight",
    "max_items_to_select",
  ]);

  var SubitemsPopupWidget = PopupWidget.extend({
    template: "SubitemsPopupWidget",
    events: _.extend({}, PopupWidget.prototype.events, {
      "click .product": "toggle_selected",
    }),
    show: function (options) {
      this.product = options.product;
      this.max_items_to_select = this.product.max_items_to_select;
      this.selected_products = new Set();
      this.selected_qty = 0;
      this.subitems = this.product.packed_product_ids.map((id) => {
        const product = this.pos.db.get_product_by_id(id);
        return {
          id: product.id,
          display_name: product.display_name,
          price: product.lst_price,
        };
      });
      this._super.apply(this, arguments);
    },
    click_confirm: function () {
      this.selected_products.forEach((id) => {
        const product = this.pos.db.get_product_by_id(id);
        this.pos.get_order().add_product(product, {
          quantity: this.product.weight / this.selected_products.size,
          merge: false,
          extras: { is_subproduct: true },
        });
      });
      this.gui.close_popup();
    },
    toggle_selected: function (event) {
      // this.selected_products is a copy of the corresponding set of the selected container
      var el_id = $(event.currentTarget).attr("data-product-id");
      var el = $(event.currentTarget);
      var wasSelected = this.selected_products.has(el_id);
      if (wasSelected) {
        this.selected_products.delete(el_id.toString());
      } else {
        if (this.selected_products.size >= this.product.max_items_to_select)
          return;
        this.selected_products.add(el_id.toString());
      }
      $("#total-flavors-selected").text(this.selected_products.size);
      el.toggleClass("selected");
    },
  });

  gui.define_popup({ name: "subitems", widget: SubitemsPopupWidget });

  screens.ProductScreenWidget.include({
    click_product: function (product) {
      if (product.to_weight && this.pos.config.iface_electronic_scale) {
        this.gui.show_screen("scale", { product: product });
      } else {
        this.pos.get_order().add_product(product, { merge: !product.is_pack });
        if (product.is_pack) {
          this.gui.show_popup("subitems", { product });
        }
      }
    },
  });
});
