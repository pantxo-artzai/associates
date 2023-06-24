from odoo import api, fields, models

class CreateSharesWizard(models.TransientModel):
    _name = 'associates.create_shares_wizard'
    _description = 'Create shares wizard'

    associate_id = fields.Many2one("associates.associate", string="Associate")
    share_type_id = fields.Many2one("associates.share.type", string="Share type")
    associate_name = fields.Char(related="associate_id.name", string="Associate Name")
    share_count = fields.Integer(string="Number of Shares", required=True)
    share_value = fields.Float(string="Share Value", required=True)
    subscription_date = fields.Date(string="Subscription Date")
    company_id = fields.Many2one("res.company", string="Company", required=True)

    contribution_type = fields.Selection([
        ('monetary_contributions', 'Monetary contributions'),
        ('non_cash_contributions', 'Non-cash contributions'),
        ], string='Contribution type')

    type = fields.Selection([
        ('subscription', 'Subscription'),
        ('other', 'Other'),
        # add more types as needed
    ], string='Type', required=True)

    def create_shares(self):
        # Créer les parts pour l'associé
        for _ in range(self.share_count):
            self.env["associates.share"].create({
                "associate_id": self.associate_id.id,
                "value": self.share_value,
                "subscription_date": self.subscription_date,
                "contribution_type": self.contribution_type,
                "share_type_id": self.share_type_id.id,
                "company_id": self.company_id.id,
            })

        # Créer une opération
        self.env["associates.operation"].create({
            "associate_id": self.associate_id.id,
            "number_of_shares": self.share_count,
            "date": self.subscription_date,
            "type": self.type,
            "amount": self.share_count * self.share_value,
            "contribution_type": self.contribution_type,
        })

        return {"type": "ir.actions.act_window_close"}
