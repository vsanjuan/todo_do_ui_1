# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Tag(models.Model):
	_name = 'todo.task.tag'
	name = fields.Char('Name', 40 , translate=True)
	# Relaltions
	task_ids = fields.Many2many('todo.task','Task')

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


