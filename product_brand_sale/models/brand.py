# -*- coding: utf-8 -*-


from odoo import models, fields, api

class SaleOrderLineInh(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', string='Brand',related="product_id.brand_id")
    brand_name = fields.Char(string='Model')
    manufacturer = fields.Char(string='Manafacturer')
    custom_charges = fields.Float(string='Custom')
    ship_charges = fields.Float(string='Shipping')
    cost = fields.Float(string='Vendor Price',readonly=True)
    margin_percent = fields.Float(string='Margin %')
    unit_pirce = fields.Float(string='Unit Price')

    @api.onchange("custom_charges","ship_charges","unit_pirce","margin_percent")
    def _onchange_prices(self):
        for i in self:
            i.cost=i.custom_charges*i.ship_charges*i.unit_pirce
            i.price_unit=int(i.cost+(i.cost*(i.margin_percent/100)))


class ProductBrand(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Brand')


class BrandProduct(models.Model):
    _name = 'product.brand'

    name = fields.Char(String="Name")
    brand_image = fields.Binary()
    member_ids = fields.One2many('product.template', 'brand_id')
    product_count = fields.Char(String='Product Count',
                                compute='get_count_products', store=True)

    @api.depends('member_ids')
    def get_count_products(self):
        self.product_count = len(self.member_ids)


class BrandPivot(models.Model):
    _inherit = 'sale.report'

    brand_id = fields.Many2one('product.brand', string='Brand')

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['brand_id'] = "t.brand_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            t.brand_id"""
        return res
