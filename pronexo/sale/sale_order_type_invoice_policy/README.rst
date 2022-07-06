.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3


================================
Sale Order Type Invoicing Policy
================================

Agregar al campo de política de facturación tipo de orden de venta con valores posibles:

* Definido por Producto: comportamiento predeterminado de odoo, la cantidad de factura se computará considerando la configuración del producto.
* Cantidades ordenadas: sobrescribe el comportamiento del producto para que todas las líneas se consideren como "cantidades pedidas" sin importar la configuración del producto, una vez que se confirma el pedido, todos los productos deben ser facturados.
* Antes de la entrega: similar a las cantidades pedidas, pero requiere una factura de pago por cada línea antes de la confirmación del pedido.
* Este módulo también está integrado con sale_usability_return_invoicing para que se puedan devolver las devoluciones de "Antes de la entrega" o "Cantidades pedidas".



* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.