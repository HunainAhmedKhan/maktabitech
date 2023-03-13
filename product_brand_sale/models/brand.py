# -*- coding: utf-8 -*-


from odoo import models, fields, api


class SaleOrderLineInh(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', string='Brand', related="product_id.brand_id")
    brand_name = fields.Char(string='Model')
    manufacturer = fields.Char(string='Manafacturer')
    custom_charges = fields.Float(string='Custom', default=1.15)
    ship_charges = fields.Float(string='Shipping', default=1.12)
    cost = fields.Float(string='Vendor Price', readonly=True)
    margin_percent = fields.Float(string='Margin %')
    unit_price = fields.Float(string='Unit Price')

    @api.onchange("custom_charges", "ship_charges", "unit_price", "margin_percent")
    def _onchange_prices(self):
        self.cost = self.custom_charges * self.ship_charges * self.unit_price
        self.price_unit = self.cost + (self.cost * (self.margin_percent / 100))

    @api.onchange("price_unit")
    def _onchange_margin(self):
        if self.cost:
            self.margin_percent =( (self.price_unit-self.cost)/(self.cost or 1))*100




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
