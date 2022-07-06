.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===========
Purchase UX
===========

Varias mejoras a las compras.

En órdenes de compra:

#. El botón de enviar por correo electrónico también está disponible en el estado finalizado de los pedidos
#. Odoo considera que una orden de compra en estado finalizado no tiene nada que facturar, cambiamos ese comportamiento para mantenerlo como órdenes de venta
#. Hacer menú de cotizaciones de compra solo visible con características técnicas
#. El menú Realizar pedidos de compra muestra todos los registros de compra (cotizaciones y confirmados)
#. Añadir estado de entrega en compras
#. Añadir impresión PO en la compra y estado hecho
#. Agregar botón para forzar "facturado" solo para admin con funciones tec
#. Botón Agregar para cambiar la moneda y actualizar los precios de las líneas de orden
#. Agregue un para filtrar por PO con devoluciones facturables.
#. Agregar enlace de facturas a las órdenes de compra que lo generan.
#. Agregue un botón "Actualizar precios de proveedores" para actualizar (o crear precios) para este proveedor y todos los productos cargados en el pedido.

En líneas de compra:

#. Agregar estado de entrega y estado de factura en líneas de compra
#. Agregue el botón en las líneas de compra para permitir que se cancele la cantidad restante.
#. Si no se define el vendedor o si el precio del vendedor es 0, se recomienda el costo contable
#. Agregue la cantidad de devolución cuando devuelva productos con la opción "Para reembolsar".

En las recogidas entrantes:

#. Agregue el botón "Agregar líneas de compra" para agregar movimientos de otras selecciones que aún están pendientes.

En las facturas de compra:

#. Agregue a la factura la función "agregar selección" en las facturas de compra, de modo que las líneas de picking que tengan alguna cantidad a facturar se agreguen. Esto es diferente a "agregar PO" que agrega todas las líneas sin importar si deben ser facturadas o no. Mantenemos esta funcionalidad porque si un proveedor le envía una factura de las mismas líneas que deben facturarse, todavía tiene la posibilidad de agregarlas.
#. Agregue un botón "Actualizar precios de proveedores" para actualizar (o crear precios) para este proveedor y todos los productos cargados en la factura.

En productos:

#. Permite buscar por proveedores y agrupar por proveedor principal en producto y variantes de producto.


* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.