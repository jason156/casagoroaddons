.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

================
Stock Request UX
================

Several improvements to Stock Request:

#. Al cancelar un request cancelamos tambien los moves encadenados.
#. Gracias a lo anterior, si cancelamos un request order se cancelan todos los pickings vinculados
#. Agregamos ruta en request order que se lleva por defecto a los request, al cambiar la ruta tambien te las cambia en los request.
#. Al crear los procurements order creamos el procurement group, propagamos que al crearse los requests tambien se lleve ese mismo group.
#. Upon duplication of request order, duplicate lines
#. Order requests from last to first created
#. Automatically reserve the picking from stock when a request is confirmed
#. Add to stock request field "order_id" ondelete=cascade to delete stock request when stock request order related are deleted.
#. Add new button in pickings to access to the stock request order if has the group "Stock Request Order"
#. Add new button in Stock moves to access to the stock request order related.

Installation
============

To install this module, you need to:

#. Only need to install the module

Configuration
=============

To configure this module, you need to:

#. No Configuration needed.

Usage
=====

To use this module, you need to:

#. Go to ...


* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.
