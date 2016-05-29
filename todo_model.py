# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import openerp.exceptions import ValidationError

class Tag(models.Model):
	_name = 'todo.task.tag'
	name = fields.Char('Name', 40 , translate=True)
	# Relations
	task_ids = fields.Many2many('todo.task','Task')
	# Hierarchical relations
	_parent_store = True
	# _parent_name = 'parent_id'
	parent_id = fields.Many2one('todo.task.tag','Parent Tag',ondelete='restrict')
	parent_left = fields.Integer('Parent Left',index=True)
	parent_right = fields.Integer('Parent Right', index=True)
	child_ids = fields.One2many('todo.task.tag','parent_id','Child Tags')

class Stage(models.Model):
	_name = 'todo.task.stage'
	_order = 'sequence,name'
	# String fields:
	name = fields.Char('Name', 40, translate=True)
	desc = fields.Text('Description')
	state = fields.Selection([('draft','New'),('open','Started'),('done','Closed')],'State')
	docs = fields.Htlm('Documentation')
	# Numeric fields:
	sequence = fields.Integer('Sequence')
	perc_complete = fields.Float('% Complete', (3,2))
	# Date fields:
	date_effective = fields.Date('Effetive Date')
	date_changed = fields.Datetime('Last Changed')
	# Other fields
	fold = fields.Boolean('Folded?')
	image = field.Binary('Image')
	# Relations
	tasks = fields.One2many('todo.task', 'stage_id','Task in this Stage')

class TodoTask(models.Model):
	_inherit = 'todo.task'
	stage_id = fields.Many2one('todo.task.stage', 'Stage')
	tags_ids = fields.Many2many('todo.task.tag', string="Tags")

	refers_to = fields.Reference([('res.user','User'),('res.partner','Partner')],'Refers to')

	stage_fold = fields.Boolean(
		'Stage Folded?',
		compute ='_compute_stage_fold',
		search = '_search_stage_fold',
		inverse = '_write_stage_fold')

	stage_state = fields.Selection(
		related = 'stage_id.state',
		string = 'Stage State')

	_sql_constrainsts = [
		('todo_task_name_uniq',
		 'UNIQUE (name, user_id, active)',
		 'Task title must be unique!')
	]

	@api.one 
	@api.constraints('name')
	def _check_name_size(self):
		if len(self.name) < 5:
			raise ValidationError('Must have 5 chars!')

	@api.one 
	@api.depends('stage_id.fold')
	def _compute_stage_fold(self):
		self.stage_fold = self.stage_id.fold

	def _search_stage_fold(self, operator, value):
		return [('stage_id.fold',operator,value)]

	def _write_stage_fold(self):
		self.stage_id.fold = self.stage_fold



