from odoo import api, fields, models


class SaleOrderLineTag(models.Model):
    _name = "sale.order.line.tag"
    _description = "Sales Order Line Tags"

    name = fields.Char(required=True)
    color = fields.Integer()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    force_line_sequence = fields.Integer()
    line_index_to_update = fields.Integer()

    def force_sequence(self):
        for rec in self:
            line_to_update = rec.order_line[rec.line_index_to_update]
            if rec.force_line_sequence and line_to_update:
                line_to_update = rec.order_line[rec.line_index_to_update]
                line_to_update.sequence = rec.force_line_sequence


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tag_ids = fields.Many2many(
        comodel_name="sale.order.line.tag", groups="sales_team.group_sale_manager"
    )

    line_number = fields.Integer(compute="_compute_line_number", store=True)

    @api.depends("order_id.order_line", "sequence")
    def _compute_line_number(self):
        order_ids = self.mapped("order_id")
        for order in order_ids:
            n = 1
            for line in order.order_line.sorted(lambda l: l.sequence):
                line.line_number = n
                n += 1

    def validate_much_doge(self, doge=None):
        """Validate Doge

        Args:
            doge (Char): doge type
        """
        if doge == "much":
            return "like"
        return "fun"
