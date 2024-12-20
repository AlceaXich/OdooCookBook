from odoo import fields, models, api


class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = "Information about hostel"
    _order = "id desc, name"
    _rec_name = 'hostel_code'

    name = fields.Char(string="Nombre del refugio", required=True)
    hostel_code = fields.Char(string="Código", required=True)
    street = fields.Char('Calle')
    street2 = fields.Char('Calle 2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('Ciudad')
    state_id = fields.Many2one("res.country.state", string='Estado')
    country_id = fields.Many2one('res.country', string='País')
    phone = fields.Char('Teléfono',required=1)
    mobile = fields.Char('Mobil',required=1)
    email = fields.Char('Email')
    hostel_floors = fields.Integer(string="Total pisos")
    image = fields.Binary('Imagen del refugio')
    active = fields.Boolean("Active", default=True,
        help="Activate/Deactivate hostel record")
    type = fields.Selection([("male", "Chicos"), ("female", "Chicas"),
        ("common", "Común")], "Tipo", help="Type of Hostel",
        required=True, default="common")
    other_info = fields.Text("Otra información",
        help="Enter more information")
    description = fields.Html('Descripción')
    hostel_rating = fields.Float('Calificación promedio', 
                                # digits=(14, 4) # Method 1: Optional precision (total, decimals),
                                 digits='Rating Value' # Method 2
                                 )
    category_id = fields.Many2one('hostel.category')
    ref_doc_id = fields.Reference(selection='_referencable_models', string='Reference Document')
    rector = fields.Many2one("res.partner", "Rector",
        help="Select hostel rector")

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.hostel_code)
            result.append((record.id, rec_name))
        return result
