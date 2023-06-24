from odoo import api, fields, models

class AssociateOperation(models.Model):
    _name = 'associates.operation'
    _description = 'Associate Operation'

    associate_id = fields.Many2one('associates.associate', string='Associate', required=True)
    date = fields.Date(string='Date', required=True)
    type = fields.Selection([
        ('subscription', 'Subscription'),
        ('other', 'Other'),
        # add more types as needed
    ], string='Type', required=True)
    number_of_shares = fields.Integer(string='Number of Shares', required=True)
    amount = fields.Float(string='Amount', required=True)
    contribution_type = fields.Selection([
        ('monetary_contributions', 'Monetary contributions'),
        ('non_cash_contributions', 'Non-cash contributions'),
    ], string='Contribution type', required=True)
    company_id = fields.Many2one("res.company", string="Related Company", required=True, default=lambda self: self.env.company)

