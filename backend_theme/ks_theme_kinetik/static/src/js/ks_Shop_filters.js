odoo.define('ks_ecommerce_theme.ks_footer', function (require) {
'use strict';

    var ajax = require('web.ajax');
    var wSaleUtils = require('website_sale.utils');
    var ks_p_id;

    $(document).ready(function(){
         $('.ks-search-clear').on("click",function(e){
         location.href='/shop';
         })
//  Handling product quantity on snippet at add to cart
//    $(document).on('click','.ks_add_to_cart',function(ev){
//            var product_id=$(ev.currentTarget).parent().find("input").val();
//            ev.preventDefault();
//            ev.stopPropagation();
//            ajax.jsonRpc("/cart/count/update", 'call', {'product_id':product_id}
//                    ).then(function(data){
//                            var quantity=data;
//                            if(quantity){
//                                if ($('#my_cart_2').length){
//                                $('#my_cart_2').removeClass('d-none');
//                                $('.my_cart_quantity').addClass('o_animate_blink');
//                                $('.my_cart_quantity').text(quantity)
//                                wSaleUtils.animateClone($('#my_cart_2'), $(ev.target).parent().closest("form"), 25, 40);
//                            }
//                            else{
//                                $('#my_cart').removeClass('d-none');
//                                $('.my_cart_quantity').addClass('o_animate_blink');
//                                $('.my_cart_quantity').text(quantity)
//                                 wSaleUtils.animateClone($('#my_cart'), $(ev.target).parent().closest("form"), 25, 40);
//                                 }
//                         }
//                    }.bind(this));
//                    return false;
//   });

    $('.o_product_info').on("click",function(e){
                $("#product_quick_preview_Modal").modal('show');
                });

    $('.product-select').on('change',function(e){
                $('.ks_text').val($( ".product-select option:selected" ).text())
                 var ks_order = $('.ks_sort_per_page').val();
                 if (ks_order !== undefined){
                $("form.js_attributes").append('<input type="hidden" name="order" value="'+ks_order+'"/>').submit();
                }
                else{
                 $("form.js_attributes").submit();
                }
                 })


    $(document).on('click', ' div.dropdown_sorty_by .dropdown-item', function (ev) {
                var order=$(ev.currentTarget).find('input').val()
                 $('.ks_sort_per_page').val(order);
                })

    $(document).ready(function(){
                  var brand=$('#ksBrandContainer').find('.active').text().trim()
                  if ($('#o_shop_collapse_category')){
                  if ( !$('#o_shop_collapse_category').find('li a.active').hasClass('o_not_editable')){
                      $('#o_shop_collapse_category').find('li a.active').addClass('ks_active')
                  }}
                  var ks_cate=$('.ks_active').text().trim();

                  _.each($('.ks_brand_active').find('input'), function(ev) {
                     if (ev){
                      $('.filter-selectedFilterContainer').removeClass('d-none');
                      $('.brand_filter_list').append('<div class="'+$(ev).val()+'"</div>')
                      $('.brand_filter').removeClass('d-none');
                      $('.'+$(ev).val()).append($(ev).parent().html());
                      $('.'+$(ev).val()).append('<span class="remove_brand_filter fa fa-times"></span>')
                      $('.'+$(ev).val()).find('input').addClass('d-none')
                      }
                        })
                    _.each($('input[name="attrib"]:checked'), function(ev) {
                     if (ev){
                       $('.filter-selectedFilterContainer').removeClass('d-none');
                      $('.variants_filter_list').append('<div class="'+$(ev).val()+'"</div>')
                      $('.variants_filter').removeClass('d-none');
                      $('.'+$(ev).val()).append($(ev).parent().html());
                      if ($(ev).attr('title')){
                      var color=$(ev).attr('title');
                      $('.'+$(ev).val()).append('<label>'+color+'</label>');
                      }
                      $('.'+$(ev).val()).append('<span class="remove_variant_filter fa fa-times"></span>')
                      $('.'+$(ev).val()).find('input').addClass('d-none')
                      }
                        })
                        if ($('select[name="attrib"]  option:selected').val()!=""){
                       _.each($('select[name="attrib"]  option:selected'), function(ev) {
                        if(ev){
                           $('.filter-selectedFilterContainer').removeClass('d-none');
                         $('.variants_filter_list').append('<div class="'+$(ev).val()+'"</div>');
                         $('.variants_filter').removeClass('d-none');
                         $('.'+$(ev).val()).append('<label>'+$(ev).text()+'</label>')
                         $('.'+$(ev).val()).append('<span class="remove_variant_filter fa fa-times"></span>')
                        }
                        })}
                  if (ks_cate){
                   $('.filter-selectedFilterContainer').removeClass('d-none');
                  $('.filterList').append('<label class="active_Category">'+'Category: </label><span class=ks-selected-items >'+ks_cate+'</span> <a class="remove_filter fa fa-times"><a/>')
                    }
                    var selected_min=parseInt($('#ks-selected_input_min_hidden').val())
                    var selected_max=parseInt($('#ks-selected_input_max_hidden').val())
                    var min=parseInt($('#ks-price-filter').attr('data-slider-min'));
                    var max=parseInt($('#ks-price-filter').attr('data-slider-max'));
                    if ((selected_min)>min | (selected_max)<max){
                                 $('.filter-selectedFilterContainer').removeClass('d-none');
                               $('.price_filter_list').append('<label id=price_list_shop>Price: </label><span class=ks-selected-items>'+selected_min+'-'+selected_max+'</span><a class="remove_price_filter fa fa-times"><a/>')
                       }
                })

     $(document).on('click','.remove_filter',function(ev){
                    $(ev.currentTarget).attr('href','/shop?'+$('.ks_active').parent().find('a').attr('href').split('?').splice(1)[0]);
                    $('.ks_active').parent().find('a').removeClass('ks_active active')
     })

     $(document).on('click','.remove_brand_filter',function(ev){
                    var brand_key=$(ev.currentTarget).parent()[0].className
                     _.each($('input[name="brnd"]:checked'), function(ev) {
                     if (ev){
                        var a=$(ev).val();
                        if (a==brand_key){
                        $(ev).attr('checked',false);
                        var ks_order = $('.ks_sort_per_page').val();
                        if (ks_order !== undefined){
                        $("form.js_attributes").append('<input type="hidden" name="order" value="'+ks_order+'"/>').submit();
                        }
                        else{
                         $("form.js_attributes").submit();
                        }
                        }
                     }
        })
     })
      $(document).on('click','.remove_price_filter',function(ev){
                    var min=parseInt($('#ks-price-filter').attr('data-slider-min'));
                    var max=parseInt($('#ks-price-filter').attr('data-slider-max'));
                    var selected_min=parseInt($('#ks-selected_input_min_hidden').val(min))
                    var selected_max=parseInt($('#ks-selected_input_max_hidden').val(max))
                    var selected_min=parseInt($('#ks-selected_input_min').val(min))
                    var selected_max=parseInt($('#ks-selected_input_max').val(max))
                    var ks_order = $('.ks_sort_per_page').val();
                     if (ks_order !== undefined){
                    $("form.js_attributes").append('<input type="hidden" name="order" value="'+ks_order+'"/>').submit();
                    }
                    else{
                     $("form.js_attributes").submit();
                 }
      })

     $(document).on('click','.remove_variant_filter',function(ev){
                    var variant_key=$(ev.currentTarget).parent()[0].className
                    _.each($('.ks_attrib_active'), function(ev) {
                     if (ev){
                        var a=$(ev).find('input').val();
                        if (a==variant_key){
                        $(ev).find('input').attr('checked',false);
                         var ks_order = $('.ks_sort_per_page').val();
                         if (ks_order !== undefined){
                         $("form.js_attributes").append('<input type="hidden" name="order" value="'+ks_order+'"/>').submit();
                          }
                        else{
                        $("form.js_attributes").submit();
                          }
                        }
              }
        })
          if ($('select[name="attrib"]  option:selected').val()!=""){
                _.each($('.ks_select_attrib option:selected'), function(ev) {
                if (ev){
                    var b=$(ev).val();
                    if (b==variant_key){
                    $(ev).attr('selected',false);
                    var ks_order = $('.ks_sort_per_page').val();
                    if (ks_order !== undefined){
                    $("form.js_attributes").append('<input type="hidden" name="order" value="'+ks_order+'"/>').submit();
                      }
                     else{
                    $("form.js_attributes").submit();
                    }
                     }
                }
         }
         )}
     })
    $("#ks-price-filter").slider({});

    $("#ks-price-filter").on("change",function(){
              if($(".is_ks_load_ajax").length === 0){
                 var ks_price_val = $("#ks-price-filter").val();
                 $("#ks-selected_input_min").val(ks_price_val[0]);
                 $("#ks-selected_input_min_hidden").val(ks_price_val[0]);
                 $("#ks-selected_input_max").val(ks_price_val[1]);
                 $("#ks-selected_input_max_hidden").val(ks_price_val[1]);
                 return false;
             }
           });

    $('.ks-price-filter-apply').on("click",function(e){
            var ks_price_val = $("#ks-price-filter").val();

            $("form.js_attributes").submit();
            return false

         });

//  this is for view mode toggling at shop page
    $('.list-view-group li').click(function(e){
                e.preventDefault();
                $(this).addClass('active');
                $('.ks-product-list').removeClass('col-lg-6')
                $('.ks-product-list').removeClass('col-lg-10')
                $('.ks-product-list').removeClass('col-lg-12')
                $('.ks-product-list').removeClass('col-lg-4')
                $('.ks-product-list').addClass('col-'+this.id)
                $(this).siblings().each(function(){
                    $(this).removeClass('active') ;
                });
       });

                var pathname = window.location.pathname;
                var parts = pathname.split("/");
                var last_part = parts[parts.length-1];
                var page = parts[2];

        if($('.ks_alternate_slider').length)
        {
            ks_p_id = last_part.split('-').pop();
            ajax.jsonRpc("/ks_product_images", 'call', {"ks_p_id":ks_p_id}).then(function (data) {
                var i;
                var info;
                var name;
                var ks_navigation;
                var ks_repeat;
                var ks_speed;
                var ks_auto;
                var ks_rtl;
                for (i = 0; i < data.length; i++)
                {
                     info =  data[i];
                     name = info['name'];
                     ks_repeat = info['ks_repeat'];
                     ks_speed = info['ks_speed'];
                     ks_auto = info['ks_auto'];
                     ks_navigation = info['ks_navigation'];
                     ks_rtl= info['rtl'];
                     if(name == "Accessories")
                     {
                          $(".accessories-prod-owl").owlCarousel({
                              items:2,
                              nav:ks_navigation,
                              autoplay:ks_auto,
                              margin:30,
                              rtl:ks_rtl,
                              loop:ks_repeat,
                              speed:ks_speed,
                           });
                     }
                     if(name == "Alternate")
                     {
                          $(".alternate-prod-owl").owlCarousel({
                              items:2,
                              autoplay:ks_auto,
                              nav:ks_navigation,
                              margin:30,
                              rtl:ks_rtl,
                              loop:ks_repeat,
                              speed:ks_speed,
                           });
                     }
                }
         });
        }
    });
});
