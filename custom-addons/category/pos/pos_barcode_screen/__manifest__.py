# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Barcode Screen",
  "summary"              :  """With the module, you can enable a separate barcode screen in the Odoo POS session. The scanned product for an order will be shown and managed here in the form of list""",
  "category"             :  "Point of Sale",
  "version"              :  "1.0.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Barcode-Screen.html",
  "description"          :  """POS Barcode Screen
POS Detailed Cart View
POS Cart Customization
POS Orderline details
POS Orderline Product
Odoo POS Barcode Screen
POS Add barcode products
POS barcode scanning
POS add product with barcode
POS user barcode scanner""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_barcode_screen&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_config_view.xml',
                             'views/template.xml',
                            ],
  "demo"                 :  ['data/pos_barcode_screen_demo.xml'],
  "qweb"                 :  ['static/src/xml/pos_barcode_screen.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  49,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}