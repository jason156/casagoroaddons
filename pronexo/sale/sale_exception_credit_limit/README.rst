.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===========================
Sale Exception Credit Limit
===========================

#. Agrega un nuevo grupo 'puede modificar el límite de crédito', solo los usuarios con este grupo pueden cambiar el límite de crédito de los socios.
#. También agrega una excepción para verificar que no pueda aprobar pedidos de venta que excedan el límite de crédito. Comprueba

* El vencimiento actual de la pareja.
* La cantidad de Órdenes de Venta aprobadas pero aún no facturadas.
* Las facturas en borrador de estado.
* El importe de la orden de venta que se va a aprobar y la compara con el límite de crédito del socio. Si el límite de crédito está por debajo de este, no es para aprobar la Orden de venta.


Instalación
============

Para instalar este módulo, necesita:

#. Solo es necesario instalar el módulo.


Configuración
=============

Para configurar este módulo, necesita:

#. Establecer 'puede modificar el límite de crédito' = verdadero o falso, en las preferencias de perfil de usuario.


* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.

