# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    cr.execute(
        """
        UPDATE product_product x SET modelo_articulo = pt.modelo_articulo
            FROM product_template pt
            JOIN product_product pp ON (pp.product_tmpl_id=pt.id) WHERE x.id = pp.id;
        """
    )
    cr.execute(
        """
        UPDATE product_template SET modelo_articulo = null;
        """
    )
