from odoo import api, fields, models

class CreateSharesWizard(models.TransientModel):
    _name = "associates.create_shares_wizard"

    associate_id = fields.Many2one("associates.associate", string="Associate")
    share_type_id = fields.Many2one("associates.share.type", string="Share type", related="associate_id.share_type_id")
    associate_name = fields.Char(related="associate_id.name", string="Associate Name")
    share_count = fields.Integer(string="Number of Shares", required=True)
    share_value = fields.Float(string="Share Value", required=True)
    subscription_date = fields.Date(string="Subscription Date")

    def create_shares(self):
        # Créer les parts pour l'associé
        for _ in range(self.share_count):
            self.env["associates.share"].create({
                "associate_id": self.associate_id.id,
                "value": self.share_value,
                "subscription_date": self.subscription_date,
            })

        return {"type": "ir.actions.act_window_close"}
