odoo.define('user_signup_approval.restrict_country', function (require) {
"use strict";
    $( document ).ready(function() {
        if ($('input#restrict_country').val()) {

            var onSuccess = function(location){
                var country_list = $('input#restrict_country').val().split(',').map(function(n) {return n;});
                if(_.contains(country_list, location.country.iso_code)) {
                    $('form').addClass('o_hidden');
                    $('div#restrict_country_message').removeClass('o_hidden')
                }
            };
            var onError = function(error){
                return
            };
            geoip2.country(onSuccess, onError);
        }
        var ajax = require('web.ajax');
        $('#tax_no').on('change', function () {
            var value = $(this).val();
            ajax.jsonRpc('/web/get_company', 'call', {'tin_no':value}).then(function (data) {
                var customer_name = $('#cust_name');
                if(data){
                	customer_name.val(data);
                }
                else {
                	alert("TIN does not exist, Unable to proceed");
                }
            });
        });
    });
})