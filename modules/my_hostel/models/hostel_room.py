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

	def find_room(self):
		#Buscar registros con search
		domain = [
			'|',
				'&', ('name', 'ilike', 'Room Name'),
					('category_id.name', 'ilike', 'Category Name'),
				'&', ('name', 'ilike', 'Second Room Name 2'),
					('category_id.name', 'ilike', 'SecondCategory Name 2')
		]
		rooms = self.search(domain)
	
	# Usando filter()
	def filter_members(self):
		#Buscamos todos los registros
		all_rooms = self.search([])
		#Llamamos al metodo para obtener los registros que cumplen con la codición
		filtered_rooms = self.rooms_with_multiple_members(all_rooms)
		print('Filtered Rooms: %s', filtered_rooms)

	@api.model
	def rooms_with_multiple_members(self, all_rooms):
		#Es una función interna que evalúa cada habitación (registro) de all_rooms.
		def predicate(room):
			if len(room.member_ids) > 1:
				return True
		#Utiliza el método filtered de Odoo para aplicar la función predicate a cada registro del conjunto all_rooms.
		#Devuelve un nuevo conjunto de registros (filtered_rooms) que cumplen la condición.
		return all_rooms.filtered(predicate)

	# Usando mapped()
	def mapped_rooms(self):
		all_rooms = self.search([])
		room_authors = self.get_member_names(all_rooms)
		print('Room Members: %s', room_authors)

	@api.model
	def get_member_names(self, all_rooms):
		#Recorre el conjunto de registros (all_rooms) y extrae los valores del campo relacionado member_ids.name.
		#Devuelve una lista con los nombres de los miembros de todas las habitaciones en all_rooms.
		return all_rooms.mapped('member_ids.name')

	# Usando sorted()
	def sort_room(self):
		all_rooms = self.search([])
		#Llama al método para ordenar las habitaciones por el campo room_rating.
		rooms_sorted = self.sort_rooms_by_rating(all_rooms)
		print('Habitaciones antes de sorted: %s', all_rooms)
		print('Habitaciones despues de sorted: %s', rooms_sorted)

	@api.model
	def sort_rooms_by_rating(self, all_rooms):
		#Ordena el conjunto de registros (all_rooms) por el campo room_rating.
		return all_rooms.sorted(key='room_rating')

class HostelRoomMember(models.Model):
	_name = 'hostel.room.member'
	_inherits = {'res.partner': 'partner_id'}
	_description = "Miembros de hostel Room"

	partner_id = fields.Many2one('res.partner', ondelete='cascade')
	date_start = fields.Date('Fecha inicio')
	date_end = fields.Date('Fecha fin')
	member_number = fields.Char()
	date_of_birth = fields.Date('Fecha de cumpleaños')