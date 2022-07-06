.. |company| replace:: pronexo.com
.. |company_logo| image:: http://fotos.subefotos.com/7107261ae57571ec94f0f2d7363aa358o.png
   :alt: pronexo.com
   :target: https://www.pronexo.com

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=========================================
Modulo Base para los Web Services de AFIP
=========================================

Homologation / production:
--------------------------
Primero busque un parámetro "afip.ws.env.type" si existe y:

* es producción -> producción
* es homologación -> homologación

Más

Busque el parámetro 'server_mode' en el archivo conf. Si ese parámetro:

* tiene un valor entonces usamos "homologación",
* Si no hay parámetro, entonces "producción"

Incluye:
--------

* Wizard para instalar los claves para acceder a las Web Services.
* API para realizar consultas en la Web Services desde OpenERP.

El módulo l10n_ar_afipws permite a Odoo acceder a los servicios del AFIP a
travésde Web Services. Este módulo es un servicio para administradores y
programadores, donde podrían configurar el servidor, la autentificación
y además tendrán acceso a una API genérica en Python para utilizar los
servicios AFIP.

Para poder ejecutar los tests es necesario cargar la clave privada y el
certificado al archivo test_key.yml.

Tenga en cuenta que estas claves son personales y pueden traer conflicto
publicarlas en los repositorios públicos.


* |company|

|company_logo|


Un Repositorio de la localización argentina.

#### Relevantes recursos addicionales, non-code
Github esta reservado al codigo, los documentos de soporte o de trabajo residen en otros lugares.