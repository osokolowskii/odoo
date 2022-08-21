from odoo import api, fields, models
import logging
import datetime

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_lines_count = fields.Integer(string="Order Lines Count", compute="_compute_order_lines_count")
    company_or_person = fields.Selection([('option1', 'Private Person'), ('option2', 'Company')], string='Customer Type', default = 'option1')
    order_lines_count_visibility = fields.Selection([('option1', 'Visible'), ('option2', 'Invisible')], string="Order Lines Counter Visibility", default='option1')
    
    @api.depends('order_line')
    def _compute_order_lines_count(self):
        for record in self:
            record.order_lines_count = len(record.order_line)
    

    @api.model
    def create(self, vals):
        vals['name'] = "CustomSO"
        res = super(SaleOrder, self).create(vals)
        
        return res
    

    def find_orders(self):
        date_range = datetime.datetime.now() - datetime.timedelta(days = 14)
        orders = self.search([('state', '=', 'draft'), ('date_order', '<=', date_range)])

        return orders

    def update_states(self):
        for record in self.find_orders():
            record.action_cancel()
       

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_type = fields.Selection([('option1', 'Food'), ('option2', 'Other')], string='Product Type', default = 'option1')