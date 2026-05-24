from odoo import models, fields
from datetime import date

class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ])

    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()

    age = fields.Integer(compute='_compute_age', store=True)

    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - (
                    (today.month, today.day) <
                    (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0