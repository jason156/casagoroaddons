odoo.define('pos_mini_tickets_report.pos', function (require) {
"use strict";

	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var models = require('point_of_sale.models');
	var Session = require('web.Session');
	var utils = require('web.utils');

    var round_di = utils.round_decimals;
	var round_pr = utils.round_precision;

	var QWeb = core.qweb;
	var _t = core._t;
    var field_utils = require('web.field_utils');

    console.log("#HOLAAAA >>>>>>>>> ");
    console.log("#MUNDO >>>>>>>>> ");

	function decimalAdjust(value){
	    var split_value = value.toFixed(2).split('.');
	    //convert string value to integer
	    for(var i=0; i < split_value.length; i++){
	        split_value[i] = parseInt(split_value[i]);
	    }
	    var reminder_value = split_value[1] % 10;
	    var division_value = parseInt(split_value[1] / 10);
	    var rounding_value;
	    var nagative_sign = false;
	    if(split_value[0] == 0 && value < 0){
	        nagative_sign = true;
	    }
	    if(_.contains(_.range(0,5), reminder_value)){
	        rounding_value = eval(split_value[0].toString() + '.' + division_value.toString() + '0' )
	    }else if(_.contains(_.range(5,10), reminder_value)){
	        rounding_value = eval(split_value[0].toString() + '.' + division_value.toString() + '5' )
	    }
	    if(nagative_sign){
	        return -rounding_value;
	    }else{
	        return rounding_value;
	    }
	}

    models.PosModel = models.PosModel.extend({
		 // return the quantity of product
            get_table_name: function(table_data){
                console.log("#### get_table_name >>> ");
                console.log("#### table_data >>> ",table_data);
                var table_name = 'N/A';
                if(table_data){
                    return table_data['name'];
                }
                return table_name;
            },
            get_number_return_list: function(qty_product){
                console.log("# get_number_return_list >>> ");
                console.log("# qty_product >>> ",qty_product);
                var lista_range = [];
                if (qty_product <= 1.0){
                     if (qty_product < 1.0){
                        return [qty_product];
                        }
                    else{
                        return [1.0];
                    }
                }else{
                    if (qty_product > 1.0 & qty_product <= 2.0){
                        return [1.0,qty_product - 1.0];
                    } else{
                        var limit_for = Math.trunc(qty_product);
                        console.log("# limit_for >>> ",limit_for);
                        for (var i=0; i < limit_for; i++){
                            lista_range.push(1.0);
                        }
                        if (qty_product - limit_for > 0.0){
                            lista_range.push(qty_product - limit_for);
                        }
                        console.log("lista_range >>",lista_range);
                        return lista_range;
                    }
                }
            },
            get_number_return_string: function(number_convert){
                /*return formats.format_value(round_di(number_convert, 2), { type: 'float', digits: [69, 2]});*/
                var amount = field_utils.format.float(round_di(number_convert, 2), {digits: [69, 2]});
                return amount;
            },
            append_list_array: function(prev_array,product_name, qty){
                console.log("function append_list_array >>");
                console.log("prev_array >>", prev_array);
                console.log("product_name >>", product_name);
                console.log("qty >>", qty);
                var new_array = prev_array;
                var new_list = [product_name, qty];
                new_array.push(new_list);
                return new_array;
            },

        });

    models.Orderline = models.Orderline.extend({
         // return the quantity of product
            get_number_return_list: function(qty_product){
                console.log("# get_number_return_list >>> ");
                console.log("# qty_product >>> ",qty_product);
                var lista_range = [];
                if (qty_product <= 1.0){
                     if (qty_product < 1.0){
                        return [qty_product];
                        }
                    else{
                        return [1.0];
                    }
                }else{
                    if (qty_product > 1.0 & qty_product <= 2.0){
                        return [1.0,qty_product - 1.0];
                    } else{
                        var limit_for = Math.trunc(qty_product);
                        console.log("# limit_for >>> ",limit_for);
                        for (var i=0; i < limit_for; i++){
                            lista_range.push(1.0);
                        }
                        if (qty_product - limit_for > 0.0){
                            lista_range.push(qty_product - limit_for);
                        }
                        console.log("lista_range >>",lista_range);
                        return lista_range;
                    }
                }
            },
            get_number_return_string: function(number_convert){
                var amount = field_utils.format.float(round_di(number_convert, 2), {digits: [69, 2]});
                /*return formats.format_value(round_di(number_convert, 2), { type: 'float', digits: [69, 2]});*/
                return amount;
            },

            append_list_array: function(prev_array,product_name, qty){
                console.log("function append_list_array >>");
                console.log("prev_array >>", prev_array);
                console.log("product_name >>", product_name);
                console.log("qty >>", qty);
                var new_array = prev_array;
                var new_list = [product_name, qty];
                new_array.push(new_list);
                return new_array;
            },

        });

});