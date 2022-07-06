var global_notification_is_first_time = true
odoo.define('advanced.notification', function (require) {
    "use strict";
    var BasicModel = require('web.BasicModel');
    var fieldRegistry = require('web.field_registry');
    var Notification = require('web.Notification');
    var relationalFields = require('web.relational_fields');
    var session = require('web.session');
    var WebClient = require('web.WebClient');
    var RecurrentNotification = Notification.extend({
        template: "RecurrentNotification",
        xmlDependencies: (Notification.prototype.xmlDependencies || [])
            .concat(['/advanced_notification/static/src/xml/template.xml']),
        init: function (parent, params) {
            this._super(parent, params);
            this.sticky = true;
            this.events = _.extend(this.events || {}, {
                'click .link2recall': function () {
                    this.close();
                },
            });
        },
    });
    WebClient.include({
        show_application: function () {
            var self = this;
            return this._super.apply(this, arguments).then(this.display_recurrent_notify.bind(this));
        },
        display_recurrent_notify: function () {
            var notifications = {
                'title': 'Reminder',
                'message': 'Please keep the following in mind:\n' +
                    '\n' +
                    'Everyone should be vigilant and take precautions to prevent the spread of viral illness: wash your hands, cough and sneeze into your elbow, and refrain from touching your face. \n' +
                    'If you are sick with a respiratory illness (cough, sneeze, breathing problems, etc.), you should stay home, avoid other people, and contact your healthcare provider if needed. All of the above precautions are of utmost importance in keeping our campus safe.\n'
            };
            var self = this;
            console.log("sdsdds")
            // var notification = false;
            // Clear previously set timeouts and destroy currently displayed recurrent notifications
            clearTimeout(this.get_next_recurrent_notif_timeout);
            _.each(this.recurrent_notif_timeouts, clearTimeout);
            var distance = 0
            if (global_notification_is_first_time) {
                global_notification_is_first_time = false
            } else {
                distance = this.get_distance_time_now();
            }
            self.recurrent_notif_timeouts = {};
            if (self.recurrent_notif == undefined || !Number.isInteger(self.recurrent_notif)) {
                self.recurrent_notif_timeouts = setTimeout(function () {
                    var notificationID = self.call('notification', 'notify', {
                        Notification: RecurrentNotification,
                        title: notifications.title,
                        message: notifications.message,
                        onClose: function () {
                            delete self.recurrent_notif;
                        },
                    });
                    self.recurrent_notif = notificationID;

                }, distance);
                // notification =  true;
            }
            distance = this.get_distance_time_now();
            this.get_next_recurrent_notif_timeout = setTimeout(this.get_next_recurrent_notify.bind(this), distance);
        },
        get_next_recurrent_notify: function () {
            this.display_recurrent_notify()
        },
        get_distance_time_now: function () {
            var now = new Date();
            var time_now = now.getHours() + now.getMinutes() / 60;
            var distance = 0
            if (time_now < 8.0) {
                distance = 8.0 - time_now;
            } else if (8.0 < time_now < 11.25) {
                distance = 11.25 - time_now;
            } else if (11.25 < time_now < 13.0) {
                distance = 13.0 - time_now;
            } else if (13.0 < time_now < 16.75) {
                distance = 16.75 - time_now;
            } else {
                // var distance = 10;
                distance = 15 * 3600.0;
            }
            distance = Math.abs(distance)
            return distance * 3600 * 1000
        }
    });
});