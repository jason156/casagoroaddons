odoo.define('edit_form_view.EditableListRenderers', function (require) {
"use strict";

var core = require('web.core');
var dom = require('web.dom');
var ListRenderer = require('web.ListRenderer');
var utils = require('web.utils');

var _t = core._t;

ListRenderer.include({
     /**
     * @private
     * @param {MouseEvent} event
     */
    _onRowClicked: function (event) {
        // The special_click property explicitely allow events to bubble all
        // the way up to bootstrap's level rather than being stopped earlier.
        if (!$(event.target).prop('special_click')) {
            var id = $(event.currentTarget).data('id');
            if (id) {
                this.trigger_up('open_record', { id: id, target: event.target, mode: 'edit'});
            }
        }
    },
});



});