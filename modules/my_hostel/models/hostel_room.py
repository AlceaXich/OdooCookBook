from odoo import fields, models, api, _

class BaseArchive(models.AbstractModel):
	_name = 'base.archive'
	active = fields.Boolean(default=True)
	
	def do_archive(self):
		for record in self:
			record.active = not record.active

class HostelRoom(models.Model):
	_name = "hostel.room"
	_description = "Imformacióndelahabitación"
	_rec_name = "room_no"

	@api.depends("student_per_room", "student_ids")
	def _compute_check_availability(self):
		"""Method to check room availability"""
		for rec in self:
			rec.availability = rec.student_per_room - len(rec.student_ids.ids)

	name = fields.Char(string="Nombre", required=True)
	room_no = fields.Char("Nro. habitación", required=True)
	floor_no = fields.Integer("Nro. piso", default=1, help="Floor Number")
	currency_id = fields.Many2one('res.currency', string='Moneda')
	rent_amount = fields.Monetary('Alquiler', help="Enter rent amount per month") # optional attribute: currency_field='currency_id' incase currency field have another name then 'currency_id'
	hostel_id = fields.Many2one("hostel.hostel", "hostel", help="Name of hostel")
	student_ids = fields.One2many("hostel.student", "room_id",
		string="Estudiantes", help="Enter students")
	hostel_amenities_ids = fields.Many2many("hostel.amenities",
		"hostel_room_amenities_rel", "room_id", "amenitiy_id",
		string="Amenities", domain="[('active', '=', True)]",
		help="Select hostel room amenities")
	student_per_room = fields.Integer("Estudiantes por habitación", required=True,
		help="Students allocated per room")
	availability = fields.Float(compute="_compute_check_availability",
		store=True, string="Availability", help="Room availability in hostel")

	_sql_constraints = [
	   ("room_no_unique", "unique(room_no)", "Room number must be unique!")]

	@api.constrains("rent_amount")
	def _check_rent_amount(self):
		"""Constraint on negative rent amount"""
		if self.rent_amount < 0:
			raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))

	def log_all_room_members(self):
		#Este metodo obtiene todos los miembros de la habitación
		#del modelo hostel.room.member
		hostel_room_obj = self.env['hostel.room.member']
		all_members = hostel_room_obj.search([])
		print("Obtenemos los registros del modelo hostel.room.member", all_members)
		return True

	def update_room_no(self):
		#Actualizar el campo room_no de una habitación
		self.ensure_one()
		self.room_no = "RM002"



class HostelRoomMember(models.Model):
	_name = 'hostel.room.member'
	_inherits = {'res.partner': 'partner_id'}
	_description = "Miembros de hostel Room"

	partner_id = fields.Many2one('res.partner', ondelete='cascade')
	date_start = fields.Date('Fecha inicio')
	date_end = fields.Date('Fecha fin')
	member_number = fields.Char()
	date_of_birth = fields.Date('Fecha de cumpleaños')