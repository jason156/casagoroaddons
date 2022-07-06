# -*- coding: utf-8 -*-
# from odoo import http
import odoo.http as http
from odoo.http import request


class AdvancedNotification(http.Controller):
    @http.route('/recurrent/notify', type='json', auth="user")
    def notify(self):
        event = True
        return {
            'title': 'Reminder',
            'message': 'Rửa tay thường xuyên: khi đến, khi chấm công, trước và sau khi ăn, khi ho, hắt hơi, khi tiếp xúc, khi đi vệ sinh'
        }