from odoo import models, fields

class HMSPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient')

    created_by = fields.Many2one('res.users')

    date = fields.Datetime(default=fields.Datetime.now)

    description = fields.Text()