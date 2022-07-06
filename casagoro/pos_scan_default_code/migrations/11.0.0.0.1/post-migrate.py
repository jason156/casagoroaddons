# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# mover el 'sale.order' patient_id a un campo de backup
# para que esto funcione, actualizar el modulo y luego desinstalarlo


def migrate(cr, version):
    cr.execute(
        """
        ALTER TABLE sale_order
        ADD COLUMN patient_id_bkp INTEGER
        """
    )

    cr.execute(
        """
        UPDATE sale_order
        SET patient_id_bkp = patient_id
        """
    )
