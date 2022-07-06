from odoo import models, api


class SiteSearchAppWebsite(models.Model):
    _inherit = 'website'

    @api.model
    def get_searchapp_styles(self):
        IrDefault = self.env['ir.default'].sudo()
        styles = IrDefault.get_model_defaults('searchapp.search.config')

        style_alignment = ''

        if styles.get('alignment') == 'center':
            style_alignment = '''#search_autocomplete .search-autocomplete {
                                         left: 50% !important;
                                        -moz-transform: translate(-50%, 0) !important;
                                        -ms-transform: translate(-50%, 0) !important;
                                        -webkit-transform: translate(-50%, 0) !important;
                                        transform: translate(-50%, 0) !important;
                                        }'''

        if styles.get('alignment') == 'left':
            style_alignment = '''#search_autocomplete .search-autocomplete {
                                        left: 0 !important;
                                        }'''

        style = '''
                #search_autocomplete .search-autocomplete{
                    border: 1px solid %s !important;
                    background-color: %s !important;
                }
                #search_autocomplete .search-title{
                    background-color: %s !important;
                }
                #search_autocomplete .search-results-list li:not(.no-results):hover{
                    background-color: %s !important;
                }
                #search_autocomplete #search-loader .lds-ellipsis div{
                    background: %s !important;
                }
                #search_autocomplete .search-title{
                    color: %s !important;
                }
                #search_autocomplete .search-results-list .price-container .price{
                    color: %s !important;
                }
                #search_autocomplete .search-results-list .product-placeholder .p-desc{
                    color: %s !important;
                }
                #search_autocomplete .search-results-list .price-container .price-slash{
                    color: %s !important;
                }
                #search_autocomplete .search-results-list .highlight{
                    color: %s !important;
                }
                %s
                %s
                ''' % (styles.get('border_color', 'transparent'), styles.get('bg_color', '#FFFFFF'),
                       styles.get('title_bg_color', '#CECECE'), styles.get('hover_color', '#EEEEEE'),
                       styles.get('loader_color', '#B6BD34'), styles.get('title_color', '#333333'),
                       styles.get('price_color', '#333333'), styles.get('text_color', '#333333'),
                       styles.get('slash_color', '#333333'), styles.get('highlight_color', '#000000'),
                       styles.get('custom_css', ''),
                       style_alignment)
        return style
