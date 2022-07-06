odoo.define('document_viewer_code', function (require) {
"use strict";

var core = require('web.core');
var Sidebar = require('web.Sidebar');
var AbstractAction = require('web.AbstractAction');

var _t = core._t;

Sidebar.include({
    start : function(){
        var self = this;
        self._super.apply(self, arguments);
        self.$el.on('click','.o_sidebar_viewer_code_item', function(evt) {
            evt.preventDefault();
            evt.stopPropagation();
            var $target = $(evt.currentTarget);
            var id = parseInt($target.attr('data-id'), 10);
            self.do_action({
                name: _t('Attachment Viewer'),
                type: 'ir.actions.client',
                tag: "document.viewer.code",
                params: {
                    id: id
                },
                target: 'new'
            });
        });
    }
});

var ViewerCode = AbstractAction.extend({
    template: "ViewerCode",
    init: function(parent, action, options) {
        var self = this;
        var url = "/web/content/" + action.params.id;
        self.url = url;
        self._super.apply(self, arguments);
    },
    start: function() {
        var self = this;
        $.get(self.url, function(code){
            hljs.highlightBlock(self.$el.find("code").text(code).get(0));
        }, "text");
        return self._super();
    },
    renderButtons: function($footer) {
        var self = this;
        $footer.hide();
    }
});

core.action_registry.add('document.viewer.code', ViewerCode);

});