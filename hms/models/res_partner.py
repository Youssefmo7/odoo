from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient'
    )

    vat = fields.Char(required=True)

    @api.constrains('related_patient_id', 'email')
    def check_customer_email(self):
        for record in self:

            if record.related_patient_id and record.email:

                patient = self.env['hms.patient'].search([
                    ('email', '=', record.email),
                    ('id', '!=', record.related_patient_id.id)
                ])

                if patient:
                    raise ValidationError(
                        'Customer email already exists in patient model'
                    )

    def unlink(self):

        for record in self:

            if record.related_patient_id:
                raise ValidationError(
                    'Cannot delete customer linked to patient'
                )

        return super().unlink()