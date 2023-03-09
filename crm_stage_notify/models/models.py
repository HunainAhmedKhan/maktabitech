# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    crm_lead_id = fields.Many2one('crm.lead')


class CrmLeadInh(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def _lang_get(self):
        return self.env['res.lang'].get_installed()

    crm_child_ids = fields.One2many('res.partner', 'crm_lead_id', string='Contact', domain=[('active', '=', True)])
    lang = fields.Selection(_lang_get, string='Language',
                            help="All the emails and documents sent to this contact will be translated in this language.")

    def write(self, vals):
        rec = super().write(vals)
        if 'stage_id' in vals:
            self._create_notification_stage_change()
        return rec

    def _create_notification_stage_change(self):
        act_type_xmlid = 'mail.mail_activity_data_todo'
        summary = 'Stage Changed'
        note = 'Stage Is changed to ' + str(self.stage_id.name)
        if act_type_xmlid:
            activity_type = self.sudo().env.ref(act_type_xmlid)
        model_id = self.env['ir.model']._get(self._name).id
        # users = self.env['res.users'].search([])
        # for rec in users:
        create_vals = {
            'activity_type_id': activity_type.id,
            'summary': summary or activity_type.summary,
            'automated': True,
            'note': note,
            'date_deadline': datetime.today(),
            'res_model_id': model_id,
            'res_id': self.id,
            'user_id': self.user_id.id,
        }
        activities = self.env['mail.activity'].create(create_vals)
