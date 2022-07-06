# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from googletrans import Translator
from odoo.exceptions import AccessError


class SystrayTranslate(models.Model):
    _name = 'systray.translate'

    @api.model
    def get_translated_text(self, text_in, destination_language, source_language):
        data = []
        try:
            if source_language is 0:
                translator = Translator()
                result = translator.translate(text_in, dest=destination_language)
                data.append(result.src)
                data.append(result.text)
                return data
            else:
                translator = Translator()
                result = translator.translate(text_in, src=source_language, dest=destination_language)
                return result.text
        except Exception:
            raise AccessError(_("Check your internet connectivity."))
