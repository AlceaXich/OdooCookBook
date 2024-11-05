from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_hostel_rector = fields.Boolean("Rector del Albergue", help="Activar si la siguiente persona es el rector del albergue")
