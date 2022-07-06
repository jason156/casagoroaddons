.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3


=========================
Purchase Suggest Extended
=========================
Este módulo es una ALTERNATIVA al módulo * procurement_suggest *; es similar, pero solo maneja las órdenes de compra y no genera ninguna adquisición: las sugerencias crean una nueva orden de compra directamente.

La ventaja es que no está afectado por las adquisiciones defectuosas (por ejemplo: una adquisición genera una orden de compra; la orden se confirma; la selección relacionada se cancela y se elimina.> ¡Las adquisiciones siempre se mantendrán en funcionamiento sin movimientos de stock relacionados!)

Para usar este módulo, debe aplicar el parche * odoo-purchase_suggest.patch * en el código fuente de Odoo.

Es posible que desee aumentar osv_memory_age_limit (valor predeterminado = 1h) en el archivo de configuración del servidor Odoo, para permitir que el usuario de la compra termine su trabajo sobre las sugerencias de compra.

Hemos realizado los siguientes cambios:

#. Añadir a la compra sugerir:
    #. Costo de reposición
    #. Reposición costo x cantidad
    #. Rotación y rotación de la ubicación
    #. pivote y vista gráfica
    #. Añadir opción para agregar productos que no tienen un punto de pedido (los valores mínimo y máximo se establecen en 0.0)

* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.