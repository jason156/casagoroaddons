odoo.define('systray.translator', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var rpc = require('web.rpc')

    var _t = core._t;
    var QWeb = core.qweb

    var options = {'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian',
                  'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian',
                  'bg': 'Bulgarian', 'ca': 'Catalan', 'ceb': 'Cebuano', 'ny': 'Chichewa',
                  'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian',
                  'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian',
                  'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician',
                  'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
                  'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian',
                  'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
                  'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'ko': 'Korean',
                  'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
                  'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay',
                  'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian',
                  'my': 'Myanmar (burmese)', 'ne': 'Nepali', 'no': 'Norwegian', 'ps': 'Pashto', 'fa': 'Persian',
                  'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian',
                  'sm': 'Samoan', 'gd': 'Scots gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi',
                  'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish',
                  'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu',
                  'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese',
                  'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
                  }

    var TranslatorItem = Widget.extend({
        template:'systray.TranslateItem',
        events: {
            "click": "on_click",
            "click #b_trans": "f_trans",
            "click #b_clear": "f_clear",
            "click #b_copy": "f_copy",
        },

        start: function(){
            this.$('#alert').hide();
            for (let key in options) {
                this.$('#src_lang').append('<option value=' + key + '>' + options[key] + '</option>');
                this.$('#dest_lang').append('<option value=' + key + '>' + options[key] + '</option>');
                this.$("#src_lang").val("sl_lang");
                this.$("#dest_lang").val("en");
            }
        },

        on_click: function (event) {
            if ($(event.target).is('i') === false) {
                event.stopPropagation();
            }
        },

        f_trans: function() {
        var text_in = $('#ip_text').val();
        var s_lang = $('#src_lang').val();
        var d_lang = $('#dest_lang').val();

        if (s_lang != 'sl_lang') {
            rpc.query({
            model: 'systray.translate',
            method: 'get_translated_text',
            args: [text_in, d_lang, s_lang]
            }).then(function(result){
                $("#op_text").val(result);
            });
        }
        else {
            rpc.query({
            model: 'systray.translate',
            method: 'get_translated_text',
            args: [text_in, d_lang, 0]
            }).then(function(data){
                $("#src_lang").val(data[0]);
                $("#op_text").val(data[1]);
            });
        }
        },

        f_copy: function() {
            $("#op_text").select();
            document.execCommand("copy");
            document.getSelection().removeAllRanges();
            $('.alert').fadeIn().delay(800).fadeOut();
        },

        f_clear: function() {
            $("#src_lang").val("sl_lang");
            $("#dest_lang").val("en");
            $("#ip_text").val("");
            $("#op_text").val("");
        },

    });

    SystrayMenu.Items.push(TranslatorItem);

    return {
        TranslatorItem: TranslatorItem,
    };
});
