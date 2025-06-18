# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint


class ProgramEvents(models.Model):
    _name = 'program.events'

    name = fields.Char('Name', required=True)
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())

class ProgramEventsGallery(models.Model):
    _name = 'program.gallery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'event_id'

    name = fields.Char('Name', readonly=True)
    date = fields.Date('Date',default=lambda self: fields.Datetime.now(), readonly=False)
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    event_id = fields.Many2one('program.events', 'Event', required=True)
    # photo_ids = fields.One2many('ir.gallery.photo','gallery_id', 'Photos')
    remarks = fields.Char('Remarks')
    attach_count = fields.Integer('Photos', compute='count_photos')


    def count_photos(self):
        for rec in self:
            rec.attach_count = self.env['ir.attachment'].search_count([('res_model', '=', 'program.gallery'), ('res_id', '=', rec.id)])


    def view_and_add_attachments(self):
        self.ensure_one()
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'program.gallery'), ('res_id', '=', self.id)])
        return {
            'name': _('View photos'),
            'view_mode': 'kanban,tree,form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            # 'context': {'default_gallery_id': self.id},
            'domain': [('id', 'in', photo_attaches.ids)],
            'target': 'current',
        }


    def get_random_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'program.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches[:4])
            return photo_attaches[:4]

    def get_current_enevt_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'program.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            return photo_attaches

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if 'name' not in vals or vals['name'] == 'New':
    #             vals['name'] = self.env['ir.sequence'].next_by_code('program.gallery') or _('New')
    #     return super().create(vals_list)


class EventsGallery(models.Model):
    _name = 'event.gallery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'event_id'

    name = fields.Char('Name', readonly=True)
    date = fields.Date('Date',default=lambda self: fields.Datetime.now(), readonly=False)
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    event_id = fields.Many2one('program.events', 'Event', required=True)
    # photo_ids = fields.One2many('ir.gallery.photo','gallery_id', 'Photos')
    remarks = fields.Char('Remarks')
    attach_count = fields.Integer('Photos', compute='count_photos')


    def count_photos(self):
        for rec in self:
            rec.attach_count = self.env['ir.attachment'].search_count([('res_model', '=', 'event.gallery'), ('res_id', '=', rec.id)])


    def view_and_add_attachments(self):
        self.ensure_one()
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'event.gallery'), ('res_id', '=', self.id)])
        return {
            'name': _('View photos'),
            'view_mode': 'kanban,tree,form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            # 'context': {'default_gallery_id': self.id},
            'domain': [('id', 'in', photo_attaches.ids)],
            'target': 'current',
        }


    def get_random_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'event.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches[:4])
            return photo_attaches[:4]

    def get_current_enevt_photos(self):
        print('SELFFFFFFFFFF',self)
        photo_attaches = self.env['ir.attachment'].search([('res_model', '=', 'event.gallery'), ('res_id', '=', self.id)])
        if photo_attaches:
            print('SSSSSAAAAAAAAAAAAAAA',photo_attaches)
            return photo_attaches

