# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLineInh(models.Model):
    _inherit = 'account.move.line'

    def get_tax_amount(self):
        tax = 0
        for l in self.tax_ids:
            tax = tax + l.amount
        tax_amount = (tax/100)* self.price_subtotal
        return tax_amount
