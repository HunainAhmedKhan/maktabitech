from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools
from odoo.exceptions import ValidationError, UserError
import json
import requests
import base64
import time
from datetime import datetime, timedelta
from datetime import date, datetime, timedelta


class CRMInht(models.Model):
    _inherit = 'crm.lead'

    deal_ids = fields.One2many('deal.evaluation', 'crm_id', string='Questions')
    score=fields.Float("Score %",compute="compute_the_total_score")
    delivery_date=fields.Date("Quotation Submission Date",default=lambda self: fields.Datetime.now())
    boq_received=fields.Boolean("Drawings/BOQ Received ?")
    lead_status= fields.Selection([
        ('1', 'Hot Lead and its In Closing Stage'),
        ('2', 'Hot Lead but still need more time / Efforts'),
        ('3', 'Warm Stage'),
        ('4', 'Cold or Early Stage - Still Not Qualified Lead')], string='Opportunity Status',
        compute='_compute_lead_status')

    lead_ready_status = fields.Selection([('1', 'On Time'),('2', 'Late')], string='Lead Status')


    def _compute_lead_status(self):
        for i in self:
          today = date.today()
          i.lead_ready_status = '1'
          if i.delivery_date:
              print(i.stage_id.name,i.delivery_date,today)
              if i.delivery_date<today and i.stage_id.name=="New":
                  i.lead_ready_status='2'

          if i.score >=75:
              i.lead_status="1"
          if i.score >60 and i.score<75:
              i.lead_status = "2"
          if i.score >50 and i.score<=60:
              i.lead_status = "3"
          if i.score <=50:
              i.lead_status = "4"

    @api.depends("deal_ids.answer_id")
    def compute_the_total_score(self):
        for i in self:
            sum=0
            for k in i.deal_ids:
                sum=sum+k.answer_id.probability
            i.score=(sum)



class dealevaluation(models.Model):
    _name = 'deal.evaluation'
    _description = "Deal Evaluation"

    crm_id=fields.Many2one("crm.lead")
    question_id=fields.Many2one("deal.questions","Questions")
    answer_id=fields.Many2one("deal.answers","Answers")

class dealQuestions(models.Model):
    _name = 'deal.questions'
    _description = "Deal Questions"

    name = fields.Char("Question")
    weight = fields.Float("Weight")
    ans_ids = fields.One2many('deal.answers', 'question_id', string='Answers')

class dealAnswers(models.Model):
    _name = 'deal.answers'
    _description = "Deal Answers"

    name = fields.Char("Answers")
    question_id = fields.Many2one("deal.questions","Deal Questions")
    percentage = fields.Float("Percentage %")
    probability = fields.Float("Probability", compute="compute_the_probability")


    @api.depends("percentage")
    def compute_the_probability(self):
        for i in self:
            i.probability=(i.question_id.weight*i.percentage)/100
