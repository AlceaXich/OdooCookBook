from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HostelCategory(models.Model):
	_name = "hostel.category"
	_description = "Hostel Categories"
	_parent_store = True
	_parent_name = "parent_id" # optional if field is 'parent_id'

	name = fields.Char('Categoría')
	parent_id = fields.Many2one(
		'hostel.category',
		string='Categoría padre',
		ondelete='restrict',
		index=True)
	parent_path = fields.Char(index=True)
	child_ids = fields.One2many(
		'hostel.category', 'parent_id',
		string='Categorías hijas')

	@api.constrains('parent_id')
	def _check_hierarchy(self):
		if not self._check_recursion():
			raise models.ValidationError('Error! You cannot create recursive categories.')

	def create_categories(self):
		#Creamos un diccionario para la primera categoria hija
		categ1 = {
			'name': 'Categoria hija 1',
			'description': 'Descripción de la categoria hija 1'
		}
		#Creamos un diccionario para la segunda categoria hija
		categ2 = {
			'name': 'Child category 2',
			'description': 'Description for child 2'
		}
		#Creamos un diccionario para la categoria principal
		parent_category_val = {
			'name': 'Categoría padre',
			'description': 'Descripción de la categoría padre',
			'child_ids': [
				(0, 0, categ1),
				(0, 0, categ2),
			]
		}
		#Llame al método create() para crear los nuevos registros
		record = self.env['hostel.room.category'].create(parent_category_val)

		#Tambien admite la creación de registros en un lote.
		#multiple_records = self.env['hostel.room.category'].create([categ1, categ2])



