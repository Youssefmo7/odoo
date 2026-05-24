from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)

    email = fields.Char(required=True)

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

    age = fields.Integer(
        compute='_compute_age',
        store=True
    )

    department_id = fields.Many2one(
        'hms.department',
        domain=[('is_opened', '=', True)]
    )

    department_capacity = fields.Integer(
        related='department_id.capacity'
    )

    doctor_ids = fields.Many2many(
        'hms.doctor'
    )

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    log_ids = fields.One2many(
        'hms.patient.log',
        'patient_id'
    )

    @api.depends('birth_date')
    def _compute_age(self):

        for record in self:

            if record.birth_date:

                today = date.today()

                record.age = (
                    today.year
                    - record.birth_date.year
                    - (
                        (today.month, today.day)
                        <
                        (
                            record.birth_date.month,
                            record.birth_date.day
                        )
                    )
                )

            else:
                record.age = 0

    @api.constrains('email')
    def check_valid_email(self):

        for record in self:

            if record.email:

                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

                if not re.match(pattern, record.email):
                    raise ValidationError(
                        'Invalid email address'
                    )

                patient = self.search([
                    ('email', '=', record.email),
                    ('id', '!=', record.id)
                ])

                if patient:
                    raise ValidationError(
                        'Email already exists'
                    )

    @api.onchange('birth_date')
    def onchange_birth_date(self):

        if self.birth_date:

            today = date.today()

            self.age = (
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    <
                    (
                        self.birth_date.month,
                        self.birth_date.day
                    )
                )
            )

            if self.age < 30:

                self.pcr = True

                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'PCR has been checked automatically'
                    }
                }

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):

        for record in self:

            if record.pcr and not record.cr_ratio:
                raise ValidationError(
                    'CR Ratio is required when PCR is checked'
                )

    def write(self, vals):

        for record in self:

            old_state = record.state

            result = super(HMSPatient, record).write(vals)

            if 'state' in vals and old_state != vals['state']:

                self.env['hms.patient.log'].create({
                    'patient_id': record.id,
                    'description': f"State changed to {vals['state']}"
                })

            return result