# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Reset Stock Move/Picking (Cancel/Reverse/Delete) in odoo",
    "version": "13.0.0.0",
    "author": "BrowseInfo",
    "category": "Warehouse",
    "website": "http://www.browseinfo.in",
    'summary': 'This module helps to reverse the done Moves, allow to cancel move and set to draft',
    "depends": [
        "stock","sale_stock","stock_picking_cancel_extended",
    ],
    "demo": [],
   'description': """


      When cancelling sale order if there are related invoices or delivery orders. 
    It automatically cancels it too. All in Cancel/Reset Orders Sales cancel Purchase cancel Delivery cancel Shipment in Odoo cancel DO
    odoo Sales Order reverse workflow odoo Sales order cancel Sale order cancel Sale cancel 
    odoo cancel Sales order cancel sale order cancel confirmed sales order cancel confirm order
    odoo set to draft sales order cancel done sales order reverse sales order process cancel confirm quotation reverse delivery order.
    odoo Sale order reverse workflow Sales reverse workflow Sale cancel Sales cancel order feature on sale
    odoo Cancel sales order Reverse sales order modify confirm sales order stock picking reverse workflow
    odoo stock picking cancel delivery order cancel incoming shipment cancel cancel picking order cancel delivery order 
    odoo cancel incoming shipment cancel order set to draft picking cancel done picking reverse picking process cancel done delivery order reverse delivery order.
    odoo stock picking reverse workflow stock picking cancel delivery order cancel delivering cancel
    odoo cancel picking order cancel delivery order cancel shipment shipment cancel order set to draft picking 
    odoo cancel done picking reverse picking process cancel done delivery order orden de entrega inversa.
    When cancelling sale order if there are related invoices or delivery orders. It automatically cancels it too.
    odoo Sales Order reverse workflow Sale order cancel Sale order cancel Sales order cancel cancel Sales order cancel sale order cancel confirmed sales order cancel 
    odoo cancel confirm order set to draft sales order cancel done sales order reverse sales order process cancel confirm quotation
    odoo reverse delivery order Sale order reverse workflow Sales reverse workflow Sale cancel Sales cancel order feature on sale. 
    odoo Cancel sales order Reverse sales order modify confirm sales order stock picking reverse workflow
    odoo stock picking cancel delivery order cancel incoming shipment cancel cancel picking order cancel delivery order
    odoo cancel incoming shipment cancel order set to draft picking cancel done picking revese picking process cancel done delivery order reverse delivery order.
    odoo stock picking reverse workflow stock picking cancel delivery order cancel delivering cancel cancel picking order cancel delivery order cancel shipment shipment cancel order set to draft picking 
    odoo cancel done picking revese picking process cancel done delivery order orden de entrega inversa.
Stock picking cancel Odoo apps is used for cancel done/validated and completed picking and set it to draft stage. Its very obvious that people or users sometimes make mistakes when working with system, When you received stock on warehouse from incoming shipment or deliver goods via delivery order and made mistakes on quantity or anything else and validate receipt or delivery then in by default odoo there is no revert option. Our Stock picking cancel Odoo apps sloved that problem and help users to cancel validated/done delivery order as well as receipt/incoming shipment.
s??lection de stock reverse workflow, s??lection de stock annuler, annulation de commande, annulation de livraison, annulation de commande, annulation de livraison, annulation de livraison, annulation de la commande, annulation de la s??lection, annulation de la pr??paration, annulation du bon de livraison. ordre de livraison inverse.
 -purchases Order reverse workflow, purchase order cancel, purchase order cancel, purchases order cancel, cancel purchases order, cancel purchase order, cancel confirmed purchases order, cancel confirm order, set to draft purchases order, cancel done purchases order, revese purchases order process, cancel confirm quotation.reverse delivery order.
    purchase order reverse workflow
purchases reverse workflow, purchase cancel, purchases cancel order feature on purchase. Cancel purchases order, Reverse purchases order
    modify confirm purchases order
    cancel stock picking , reset all orders
    odoo cancel and reset to draft picking cancel reset picking cancel picking cancel delivery order
    odoo cancel incoming shipment reverse stock picking reverse delivery order Cancel invoice based on sales
    odoo cancel invoice based on purchase cancel all in one order cancel all orders
    odoo all order cancel all order reset all order reverse reverse order all in one

odoo stock inventory reverse workflow stock inventory cancel inventory adjustment cancel incoming shipment cancel 
odoo cancel inventory adjustment cancel delivery order cancel incoming shipment cancel order set to draft picking cancel done picking revese picking process 
odoo cancel done delivery order reverse delivery order stock inventory adjustment reverse workflow stock inventory adjustment cancel
odoo stock adjustment reverse workflow warehouse stock cancel stock warehouse cancel cancel stock for inventory cancel stock inventory cancel inventory adjustment from done state 
odoo cancel warehouse stock adjustment cancel order set to draft picking cancel done picking revese picking process cancel done delivery order. 
odoo orden de entrega inversa s??lection de stock reverse workflow s??lection de stock annuler 
annulation de commande annulation de livraison annulation de commande annulation de livraison annulation de livraison
 annulation de la commande annulation de la s??lection annulation de la pr??paration annulation du bon de livraison. ordre de livraison inverse.
 odoo cancel stock Inventory Adjustment cancel and reset to draft Inventory Adjustment odoo cancel reset Inventory Adjustment 
 odoo cancel Inventory Adjustment cancel delivery stock Adjustment cancel stock Adjustment
odoo reverse Inventory Adjustment reverse stock Inventory Adjustment
odoo cancel orders order cancel odoo cancel picking odoo cancel stock move odoo stock move cancel
odoo Inventory Adjustment Cancel Cancel Inventory Adjustment delivery cancel
odoo picking cancel Reverse order reverse picking reverse delivery reverse shipment
odoo stock move reverse workflow stock move cancel delivery order cancel incoming shipment cancel cancel picking order cancel delivery order cancel incoming shipment cancel order 
odoo set to draft move cancel done move reverse picking process cancel done delivery order reverse delivery order.
roll back stock move roll back picking order in odoo cancel incoming shipment cancel stock move roll back shipment
stock move reverse workflow, stock move cancel, delivery order cancel, delivering cancel, cancel picking order, cancel delivery order, cancel shipment shipment, cancel order, set to draft move, cancel done move, revese move process, cancel done delivery order. orden de entrega inversa.
Reset Stock moves Reset Inventory moves Reset Stock inventory moves Reset stock picking moves Reset stock Inventory moves Reset inventory picking.
Reset Delivery Orders Reset Incoming shipments Reset picking moves Reset orders.
Delete Stock moves delete Inventory moves delete Stock inventory moves delete stock picking moves delete stock Inventory moves delete inventory picking.
Reverse Stock moves Reverse Inventory moves Reverse Stock inventory moves Reverse stock picking moves Reverse stock Inventory moves Reverse inventory picking.
s??lection de stock reverse workflow, s??lection de stock annuler, annulation de commande, annulation de livraison, annulation de commande, annulation de livraison, annulation de livraison, annulation de la commande, annulation de la s??lection, annulation de la pr??paration, annulation du bon de livraison. ordre de livraison inverse.

-stock mover flujo de trabajo inverso, stock movimiento cancelar, orden de entrega cancelar, env??o entrante cancelar, cancelar pedido, cancelar pedido, cancelar env??o entrante, cancelar pedido, establecer movimiento borrador, cancelar movimiento hecho, proceso de selecci??n inversa, cancelar orden de entrega . orden de entrega inversa.

stock mover flujo de trabajo inverso, mover stock cancelar, cancelar pedido, entregar cancelar, cancelar pedido de picking, cancelar pedido de entrega, cancelar env??o de env??o, cancelar pedido, establecer borrador de movimiento, cancelar movimiento hecho, reverencia proceso de movimiento, cancelar orden de entrega realizada. orden de entrega inversa.
Restablecer movimientos de stock, restablecer movimientos de inventario, restablecer movimientos de stock de inventario, restablecer movimientos de stock picking, restablecer stock movimientos de inventario, restablecer inventario picking.
Restablecer pedidos de entrega, restablecer env??os entrantes, restablecer movimientos de selecci??n, restablecer pedidos.
Eliminar movimientos de stock, eliminar movimientos de inventario, eliminar movimientos de stock de inventario, eliminar movimientos de stock picking, eliminar stock movimientos de inventario, eliminar picking de inventario.
Invertir movimientos de stock, Invertir movimientos de inventario, Invertir movimientos de stock de inventario, Invertir movimientos de stock de stock, Invertir stock Movimientos de inventario, Invertir inventario de picking.

-stock d??placer le flux de travail inverse, annuler le mouvement stock, annuler la commande, annuler l'envoi, annuler l'ordre de pr??l??vement, annuler l'ordre de livraison, annuler l'envoi entrant, annuler l'ordre, annuler le d??m??nagement, annuler le pr??l??vement, annuler l'ordre de livraison ordre de livraison inverse.

mouvement de stock inverse workflow, annulation de mouvement stock, annulation de commande, annulation de livraison, annulation de commande, annulation de livraison, annulation de livraison, annulation de commande, annulation de mouvement, annulation du processus de d??m??nagement, annulation du bon de livraison. orden de entrega inversa.
R??initialiser les mouvements de stock, R??initialiser les mouvements d'inventaire, R??initialiser les mouvements de stock, R??initialiser les mouvements de s??lection de stock, R??initialiser les mouvements d'inventaire, R??initialiser la s??lection de stock.
R??initialiser les commandes de livraison, R??initialiser les envois entrants, R??initialiser les mouvements de pr??l??vement, R??initialiser les commandes.
Supprimer les mouvements de stock, supprimer les mouvements d'inventaire, supprimer les mouvements de stock, supprimer les mouvements de s??lection de stock, supprimer les mouvements d'inventaire, supprimer la s??lection de stock.
Les mouvements de stocks invers??s, les mouvements de stocks invers??s, les mouvements de stocks invers??s, les mouvements de s??lection de titres invers??s, les mouvements de stocks invers??s, la s??lection inverse de stocks.

    When cancelling sale order if there are related invoices or delivery orders. 
    It automatically cancels it too. All in Cancel/Reset Orders Sales cancel Purchase cancel Delivery cancel Shipment in Odoo cancel DO
    odoo Sales Order reverse workflow odoo Sales order cancel Sale order cancel Sale cancel 
    odoo cancel Sales order cancel sale order cancel confirmed sales order cancel confirm order
    odoo set to draft sales order cancel done sales order reverse sales order process cancel confirm quotation reverse delivery order.
    odoo Sale order reverse workflow Sales reverse workflow Sale cancel Sales cancel order feature on sale
    odoo Cancel sales order Reverse sales order modify confirm sales order stock picking reverse workflow
    odoo stock picking cancel delivery order cancel incoming shipment cancel cancel picking order cancel delivery order 
    odoo cancel incoming shipment cancel order set to draft picking cancel done picking reverse picking process cancel done delivery order reverse delivery order.
    odoo stock picking reverse workflow stock picking cancel delivery order cancel delivering cancel
    odoo cancel picking order cancel delivery order cancel shipment shipment cancel order set to draft picking 
    odoo cancel done picking reverse picking process cancel done delivery order orden de entrega inversa.
    When cancelling sale order if there are related invoices or delivery orders. It automatically cancels it too.
    odoo Sales Order reverse workflow Sale order cancel Sale order cancel Sales order cancel cancel Sales order cancel sale order cancel confirmed sales order cancel 
    odoo cancel confirm order set to draft sales order cancel done sales order reverse sales order process cancel confirm quotation
    odoo reverse delivery order Sale order reverse workflow Sales reverse workflow Sale cancel Sales cancel order feature on sale. 
    odoo Cancel sales order Reverse sales order modify confirm sales order stock picking reverse workflow
    odoo stock picking cancel delivery order cancel incoming shipment cancel cancel picking order cancel delivery order
    odoo cancel incoming shipment cancel order set to draft picking cancel done picking revese picking process cancel done delivery order reverse delivery order.
    odoo stock picking reverse workflow stock picking cancel delivery order cancel delivering cancel cancel picking order cancel delivery order cancel shipment shipment cancel order set to draft picking 
    odoo cancel done picking revese picking process cancel done delivery order orden de entrega inversa.
Stock picking cancel Odoo apps is used for cancel done/validated and completed picking and set it to draft stage. Its very obvious that people or users sometimes make mistakes when working with system, When you received stock on warehouse from incoming shipment or deliver goods via delivery order and made mistakes on quantity or anything else and validate receipt or delivery then in by default odoo there is no revert option. Our Stock picking cancel Odoo apps sloved that problem and help users to cancel validated/done delivery order as well as receipt/incoming shipment.
s??lection de stock reverse workflow, s??lection de stock annuler, annulation de commande, annulation de livraison, annulation de commande, annulation de livraison, annulation de livraison, annulation de la commande, annulation de la s??lection, annulation de la pr??paration, annulation du bon de livraison. ordre de livraison inverse.
 -purchases Order reverse workflow, purchase order cancel, purchase order cancel, purchases order cancel, cancel purchases order, cancel purchase order, cancel confirmed purchases order, cancel confirm order, set to draft purchases order, cancel done purchases order, revese purchases order process, cancel confirm quotation.reverse delivery order.
    purchase order reverse workflow
purchases reverse workflow, purchase cancel, purchases cancel order feature on purchase. Cancel purchases order, Reverse purchases order
    modify confirm purchases order
    cancel stock picking , reset all orders
    odoo cancel and reset to draft picking cancel reset picking cancel picking cancel delivery order
    odoo cancel incoming shipment reverse stock picking reverse delivery order Cancel invoice based on sales
    odoo cancel invoice based on purchase cancel all in one order cancel all orders
    odoo all order cancel all order reset all order reverse reverse order all in one

odoo stock inventory reverse workflow stock inventory cancel inventory adjustment cancel incoming shipment cancel 
odoo cancel inventory adjustment cancel delivery order cancel incoming shipment cancel order set to draft picking cancel done picking revese picking process 
odoo cancel done delivery order reverse delivery order stock inventory adjustment reverse workflow stock inventory adjustment cancel
odoo stock adjustment reverse workflow warehouse stock cancel stock warehouse cancel cancel stock for inventory cancel stock inventory cancel inventory adjustment from done state 
odoo cancel warehouse stock adjustment cancel order set to draft picking cancel done picking revese picking process cancel done delivery order. 
odoo orden de entrega inversa s??lection de stock reverse workflow s??lection de stock annuler 
annulation de commande annulation de livraison annulation de commande annulation de livraison annulation de livraison
 annulation de la commande annulation de la s??lection annulation de la pr??paration annulation du bon de livraison. ordre de livraison inverse.
 odoo cancel stock Inventory Adjustment cancel and reset to draft Inventory Adjustment odoo cancel reset Inventory Adjustment 
 odoo cancel Inventory Adjustment cancel delivery stock Adjustment cancel stock Adjustment
odoo reverse Inventory Adjustment reverse stock Inventory Adjustment
odoo cancel orders order cancel odoo cancel picking odoo cancel stock move odoo stock move cancel
odoo Inventory Adjustment Cancel Cancel Inventory Adjustment delivery cancel
odoo picking cancel Reverse order reverse picking reverse delivery reverse shipment

-?????????? ???????? ?????? ?????????? ???????????? ?? ?????? ???????????? ?????????? ?? ?????????? ?????????? ?????????????? ?? ?????? ?????????????? ?? ?????????? ?????????? ???????????????? ?? ?????????? ?????????? ?????????????? ?? ?????????? ???????? ?????????? ?? ?????????? ?????????? ?? ?????????? ?????? ???????????? move ?? ?????????? ?????????? ???????? ???? ???????????? ?? ?????????? ?????????? ?????????? ?????????????? ?? ?????????? ?????? ?????????????? . ?????????? ?????????????? ????????????.

???????????? ?????????? ?????? ?????????? ???????????? ?? ?????? ???????????? ?????????? ?? ?????????? ?????????? ?????????????? ?? ?????????? ?????????? ?? ?????????? ?????????? ???????????????? ?? ?????????? ?????????? ?????????????? ?? ?????????? ???????? ???????????? ?? ?????????? ?????????? ?? ?????????? ?????? ???????????? ???????????? ?? ?????????? ???????????? ?????? ?? ?????????? ???????????????? ???????? ?? ?????????? ?????????? ??????????????. orden de entrega inversa.
?????????? ?????????? ???????? ?????????????? ?? ?????????? ?????? ???????????????? ?? ?????????? ?????? ?????????? ?????????????? ?? ?????????? ?????????? ???????????? ???????????? ???????????? ?? ?????????? ?????????? ?????????? ???????????????? ?? ?????????? ?????????? ?????? ??????????????.
?????????? ?????????? ?????????????? ?? ?????????? ?????????? ?????????????? ?????????????? ?? ?????????? ?????????? ???????????????? ?? ?????????? ?????????? ??????????????.
?????? ???????????? ?????????????? ?? ?????? ???????????? ?????????????? ?? ?????? ???????????? ?????????????? ?????????????? ?? ?????? ???????????? ?????? ???????????? ?? ?????? ?????????????? ?????????? ?????????????? ?? ?????? ?????? ??????????????.
???????????? ???????????? ?????????????? ?? ???????????????? ?????????????? ?????????????? ?? ???????????? ?????????? ?????????????? ???????????? ?? ???????????????? ???????????????? ???????????? ?????????????? ?? ???????????????? ?????????????? ???????? ?????????????? ?? ???????????? ?????????????? ????????????.

-stock move o fluxo de trabalho reverso, cancelamento de movimento de estoque, cancelamento de pedido de entrega, cancelamento de remessa recebida, cancelamento de pedido de picking, cancelamento de pedido de remessa, cancelamento de remessa recebida, cancelamento de pedido, ajuste de rascunho ordem de entrega reversa.

movimento de estoque fluxo reverso, cancelamento de movimento de estoque, cancelamento de pedido de entrega, cancelamento de entrega, cancelamento de pedido de picking, cancelamento de pedido de remessa, cancelamento de remessa de remessa, cancelamento de pedido, ajuste para rascunho de movimento, cancelamento de movimento, cancelamento de entrega. orden de entrega inversa.
Redefinir a????es, redefinir Movimentos de invent??rio, Redefinir Movimentos de estoque, Redefinir movimenta????es de estoque, Reajustar estoque Movimentos de estoque, Redefinir picking de invent??rio.
Redefinir ordens de entrega, redefinir remessas recebidas, redefinir movimentos de picking, redefinir pedidos.
Eliminar movimentos de estoque, excluir movimentos de estoque, excluir movimentos de estoque, eliminar movimentos de picking de estoque, eliminar estoque Movimentos de estoque, excluir picking de estoque.
Estoque reverso de estoque, Movimentos de estoque reversos, Reversos Movimentos de estoque, Movimentos reversos de picking de estoque, Estoque inverso Movimentos de estoque, Invent??rio reverso de estoque.

    """,
    'price': 40,
    'currency': "EUR",
    "data": [
        "security/move_security.xml",
        "views/stock_move_view.xml"
    ],
    'live_test_url':'https://www.youtube.com/watch?v=lY6Jb8sml0E',
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,
    "images":["static/description/Banner.png"],
}
