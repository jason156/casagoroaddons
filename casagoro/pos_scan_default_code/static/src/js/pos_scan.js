odoo.define('pos_scan_default_code', function (require) {
    "use strict";
var rpc = require('web.rpc');
var models = require('point_of_sale.models');
var DB = require('point_of_sale.DB');
var utils = require('web.utils');
models.load_fields("product.product", ['modelo_articulo']);
var _super = DB.prototype;

var core = require('web.core');
var _t = core._t;
var QWeb = core.qweb;

var _super_posmodel = models.PosModel.prototype;
models.PosModel = models.PosModel.extend({
    initialize: function(session, attributes) {
        _super_posmodel.initialize.apply(this, arguments);
        var self = this;
        this.packages = [];
    },
    scan_product: function(parsed_code){
        console.log("scan")
        var selectedOrder = this.get_order();
        var pro_package = this.db.get_packaging_by_barcode(parsed_code)
        if (!pro_package){
            console.log(pro_package)
            console.log("super")
            return _super_posmodel.scan_product.apply(this, arguments);
        }
        else{
            for(var i = 0, len=pro_package.qty; i < len; i++){
                console.log("for")
                console.log(pro_package.product_id)
                selectedOrder.add_product(this.db.get_product_by_id(pro_package.product_id[0]));
            }
            return true;
        }
        }
    });

models.load_models({
        model: 'product.packaging',
        fields: ['id','product_id', 'barcode', 'qty'],
        domain: [],
        loaded: function(self, packages) {
            self.packages = packages;
            self.db.add_pakaging(packages);
        }
    });

DB.include({
    init: function(options){
        this._super.apply(this, arguments);
        this.product_packaging_by_barcode = {};
    },
    add_products: function(products){
        var res = this._super(products);

        if(!products instanceof Array){
            products = [products];
        }
        for(var i = 0, len = products.length; i < len; i++){
            var product = products[i];
            if(product.default_code){
                this.product_by_barcode[product.default_code] = product;
            }
        }
    },
    add_pakaging: function(packages){
        if(!packages instanceof Array){
            packages = [pakages]
        }
        for(var i = 0, len = packages.length; i < len; i++){
            var pro_package = packages[i]
            this.product_packaging_by_barcode[pro_package.barcode] = pro_package
        }
    },
    get_packaging_by_barcode: function(barcode){
        if(this.product_packaging_by_barcode[barcode.code]){
            return this.product_packaging_by_barcode[barcode.code];
        } else {
            return undefined;
        }
    },
    _product_search_string: function(product){
        var str = product.display_name;
        if (product.barcode) {
            str += '|' + product.barcode;
        }
        if (product.default_code) {
            str += '|' + product.default_code;
        }
        if (product.description) {
            str += '|' + product.description;
        }
        if (product.description_sale) {
            str += '|' + product.description_sale;
        }
        if (product.modelo_articulo) {
            str += '|' + product.modelo_articulo;
        }
        str  = product.id + ':' + str.replace(/:/g,'') + '\n';
        return str;
    },
    });
});
