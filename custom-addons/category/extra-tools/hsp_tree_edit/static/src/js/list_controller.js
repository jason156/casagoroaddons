odoo.define('hsp_tree_edit.ListController', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');


    var _t = core._t;

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this,arguments);
            if (this.$buttons=== undefined){
                return
            }
            this.hsp_longpress = 1000;
            this.hsp_start = 0;
            this.hsp_editable_btn = $('<button type="button" style="color: #6c757d;" class="btn btn-secondary fa fa-pencil hsp_editable_btn" title="编辑" style="position: relative;"></button>')
            this.hsp_editable_btn.appendTo(this.$buttons)
            // this.$buttons.on('click', '.hsp_editable_btn', this._onHspEditableBtn.bind(this));
            
            this.$buttons.on('mousedown', '.hsp_editable_btn', this._onHspMousedown.bind(this));
            this.$buttons.on('mouseleave', '.hsp_editable_btn', this._onMouseleave.bind(this));
            this.$buttons.on('mouseup', '.hsp_editable_btn', this._onMouseup.bind(this));
            if(typeof this.renderer.isMultiEditable === 'undefined' || this.renderer.isMultiEditable == false){
            }else{
                this.hsp_editable_btn.attr('style', "color: #f0ad4e;");
            }
        },
        // _onHspEditableBtn: function(){
        //     if(typeof this.renderer.editable === 'undefined' || this.renderer.editable == false){
        //         this.renderer.editable=true
        //         this.hsp_editable_btn.attr('style', "color: #00a09d;");
        //     }else{
        //         this.renderer.editable=false
        //         this.hsp_editable_btn.attr('style', "color: #6c757d;");
        //     }
        // },

        _onHspMousedown:function(){
            this.hsp_start = new Date().getTime();
        },
        _onMouseleave:function(){
            this.hsp_start = 0;
        },
        _onMouseup:function(){
            if ( new Date().getTime() >= ( this.hsp_start + this.hsp_longpress )) {
                //long press
                console.log(this.renderer.isMultiEditable)
                if(typeof this.renderer.isMultiEditable === 'undefined' || this.renderer.isMultiEditable == false){
                    this.renderer.isMultiEditable = true
                    this.renderer.editable = true
                    this.hsp_editable_btn.attr('style', "color: red;");
                }else{
                    this.renderer.editable=false
                    this.renderer.isMultiEditable = false
                    this.hsp_editable_btn.attr('style', "color: #6c757d;");
                }
             } else {
                 //short press
                if(typeof this.renderer.editable === 'undefined' || this.renderer.editable == false){
                    this.renderer.editable=true
                    this.renderer.isMultiEditable = false
                    this.hsp_editable_btn.attr('style', "color: #00a09d;");
                }else{
                    this.renderer.editable=false
                    this.renderer.isMultiEditable = false
                    this.hsp_editable_btn.attr('style', "color: #6c757d;");
                }
             }
             this.hsp_start = 0;
        }

    })
});
