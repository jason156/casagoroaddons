.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3


===================================
Product Price Taxes Included or Not
===================================

Este módulo le permite ver los precios de los productos con o sin impuestos incluidos.

#. Cree un nuevo campo en los productos que se muestra en el árbol y la forma que muestra "Precio del producto" con impuestos incluidos (en las versiones anteriores era el mismo campo lst_price, pero luego no podía buscar y clasificar por este campo, por lo que para la confidencialidad mantenemos el odoo nativo campos y añadir nuestros propios)
#. También modifique el método de listas de precios para que, si se envían include_taxes en el contexto, obtendrá precios con impuestos incluidos

Instalación
============

Para instalar este módulo, necesita:

#. Sólo instale el módulo.

Configuración
=============

Para configurar este módulo, necesita:

#. No se necesita configuración.

Uso
=====

#. En la vista de formulario se agrega un nuevo campo con los impuestos incluidos.
#. En el árbol de productos y en la vista de Kanban si agrega el filtro "Impuestos incluidos",
    Luego se muestran los precios con impuestos incluidos.

* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.