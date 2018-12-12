from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Covers(models.Model):
    _name='coverage.line'

    _rec_name='proposal_id'

    covers_crm=fields.Many2one('crm.lead','covers opp')
    proposal_id=fields.Many2one('proposal.opp.bb','Proposal')
    risk_id_covers = fields.Many2one('crm.risk', 'Risk')
    # risk_desc=fields.Char('Risk Description')
    # Company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer")
    # product_pol = fields.Many2one('insurance.product', domain="[('insurer','=',Company)]", string="Product")
    insurer = fields.Many2one(related='proposal_id.Company')
    product = fields.Many2one(related='proposal_id.product_pol',domain="[('insurer','=',insurer)]")
    covers=fields.Many2one('insurance.product.coverage',domain="[('product_id','=',product)]")
    sum_insured=fields.Float('SI')
    deductible = fields.Float('Deductible')
    limitone = fields.Float('Limit in One')
    limittotal = fields.Float('Limit in Total')
    rate=fields.Float('Rate')
    net_premium=fields.Float('Net Premium')
    check=fields.Boolean(related='covers.readonly')


    @api.onchange('proposal_id')
    def onchange_proposal_id(self):
        if self.covers_crm :
            return {'domain':{'proposal_id': [('id','in',self.covers_crm.proposal_opp.ids)]}}

    @api.onchange('risk_id_covers')
    def onchange_risk(self):
        if self.covers_crm:
            return {'domain': {'risk_id_covers': [('id', 'in', self.covers_crm.objectrisks.ids)]}}


    @api.onchange('covers')
    def onchange_covers(self):
            if self.covers:
               self.sum_insured=self.covers.defaultvalue
               self.deductible=self.covers.deductible
               self.limitone=self.covers.limitone
               self.limittotal=self.covers.limittotal

    @api.onchange('rate','sum_insured')
    def compute_premium(self):
        if self.covers and self.rate:
               self.net_premium=(self.sum_insured*self.rate)/100






    # @api.onchange('risk_id_covers')
    # def onchange_risc_desc(self):
    #     if self.risk_id_covers:
    #         self.risk_desc=self.risk_id_covers.risk_description


