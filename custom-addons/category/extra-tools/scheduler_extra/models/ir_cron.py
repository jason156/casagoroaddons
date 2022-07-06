import logging
from datetime import datetime, timedelta

from odoo import models


class IrCron(models.Model):
    _inherit = "ir.cron"

    def batch_reschedule(self, interval=600, delay=10):
        nextcall = datetime.now() + timedelta(seconds=delay)

        for rec in self:
            logging.info("Rescheduling cron %s at %s.", rec.name, next)
            rec.write({"nextcall": nextcall})
            nextcall += timedelta(seconds=interval)

        return True
