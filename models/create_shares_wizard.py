from odoo import api, fields, models

class CreateSharesWizard(models.TransientModel):
    _name = "associates.create_shares_wizard"

    associate_id = fields.Many2one("associates.associate", string="Associate")
    associate_name = fields.Char(related="associate_id.name", string="Associate Name", readonly=True)
    share_count = fields.Integer(string="Number of Shares", required=True)
    share_value = fields.Float(string="Share Value", required=True)

    def create_shares(self):
        # Créer les parts pour l'associé
        for _ in range(self.share_count):
            self.env["associates.share"].create({
                "associate_id": self.associate_id.id,
                "value": self.share_value,
            })

        return {"type": "ir.actions.act_window_close"}
