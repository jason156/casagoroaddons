.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==========================
Product Replenishment Cost
==========================

Proporciona un método reemplazable en el producto que computa el costo de reposición de un producto. De forma predeterminada, solo devuelve el valor del campo "Precio de costo", pero al utilizar el módulo product_cost_incl_bom, devolverá el cálculo del costo desde el bom.

Como es un módulo genérico, también puede configurar su propia forma de calcular el costo de reposición para su producto.

#. Todos los módulos OCA para calcular márgenes se basan en él, por lo que podrá usarlos a su manera.
#. Nuevo costo de reposición Última actualización
#. Seguimiento de los cambios de RC (costo de reposición) Última actualización, costo base RC, moneda de costo base RC
#. Actualizar RC Última actualización automáticamente si se modifica el Costo base RC o el Costo base RC (NOTA: no se realiza un seguimiento de los cambios en el cambio de moneda)
#. Añadir reglas de costo de reafirmación de productos. Cada regla puede tener varias líneas, cada línea puede agregar un porcentaje y una cantidad fija. También actualiza "Última actualización de RC" automáticamente si la regla o las líneas de la regla cambian. También los cambios en las líneas de reglas se rastrean dentro de las reglas.
#. Agregue las reglas de costo de Replenshiment a supplierinfo.
#. Puede seleccionar "Tipo de costo de reaprovisionamiento" para usar las reglas de costo de Replenshiment en el producto o las reglas de uso en supplierinfo para el primer vendedor.
#. Ahora, cuando cree una Orden de Compra, el precio que se sugiere en la línea es el costo de replanificación.Provides an overridable method on product which compute the Replenishment cost of a product. By default it just returns the value of "Cost price" field, but using the product_cost_incl_bom module, it will return the costing from the bom.

As it is a generic module, you can also setup your own way of computing the replenishment_cost for your product.

#. All OCA modules to compute margins are based on it, so you'll be able to use them in your own way.
#. New Replenishment Cost Last Update
#. Track changes of RC (Replenishment Cost) Last update, RC Base Cost, RC Base Cost Currency
#. Update RC Last Update automatically if RC Base Cost or RC Base Cost Currency changes (NOTE: currency exchange changes are not tracked)
#. Add Product Replenshiment Cost Rules. Each rule can have several lines, each line can add a percentage and a fixed amount. It also update "RC Last Update" automatically if rule or rule lines change. Also changes in rules lines are tracked inside the rules.
#. Add Replenshiment cost rules to supplierinfo.
#. You can select "Replenishment Cost Type" to use Replenshiment cost rules in the product or use rules in supplierinfo for the first seller.
#. Now when create an Purchase Order the price that suggest in the line is the replanishment cost.


* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.