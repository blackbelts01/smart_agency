from odoo import models, fields, api
from odoo.exceptions import ValidationError



class inhertResPartner(models.Model):
    _inherit = 'res.partner'

    insurer_type=fields.Boolean('Insurer')
    agent=fields.Boolean('Agent')
    insurer_branch=fields.Many2one("res.partner",string="Insurer Branch")
    holding_type=fields.Boolean("Holding")
    holding_company=fields.Many2one("res.partner",string="Holding Company")
    numberofchildren=fields.Integer('Number of Children')
    policy_count=fields.Integer(compute='_compute_policy_count')


    brok_inv_count=fields.Integer(compute='_compute_brok_inv_count')
    prem_bill_count=fields.Integer(compute='_compute_prem_bill_count')

    opp_count = fields.Integer(compute='_compute_opp_count')

    C_industry=fields.Many2one('insurance.setup.item',string='Industry',domain="[('setup_id.setup_key','=','industry')]")
    DOB=fields.Date('Date of Birth')
    martiual_status = fields.Selection([('Single', 'Single'),
                                        ('Married', 'Married'),],
                                       'Marital Status', track_visibility='onchange')
    last_time_insure = fields.Date('Last Time Insure')

    @api.one
    def _compute_policy_count(self):
        if self.customer == 1:
            for partner in self:
                operator = 'child_of' if partner.is_company else '='
                partner.policy_count = self.env['policy.broker'].search_count(
                    [('customer', operator, partner.id)])

        elif self.insurer_type == 1:
            for partner in self:
                operator = 'child_of' if partner.is_company else '='
                partner.policy_count = self.env['policy.broker'].search_count(
                    [('company', operator, partner.id)])
        elif self.agent == 1:
            for partner in self:
                operator = 'child_of' if partner.is_company else '='
                partner.policy_count = self.env['policy.broker'].search_count(
                    [('salesperson', operator, partner.id)])
    @api.multi
    def show_partner_policies(self):
        if self.customer == 1:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'policy.broker',  # model name ?yes true ok
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {'default_customer': self.id},
                'domain': [('customer', '=', self.id)]
            }
        elif self.insurer_type == 1:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'policy.broker',  # model name ?yes true ok
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {'default_company': self.id},
                'domain': [('company', '=', self.id)]
            }
        elif self.agent == 1:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'policy.broker',  # model name ?yes true ok
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {'default_salesperson': self.id},
                'domain': [('salesperson', '=', self.id)]
            }

    @api.one
    def _compute_opp_count(self):
        if self.customer == 1:
            for partner in self:
                operator = 'child_of' if partner.is_company else '='
                partner.opp_count = self.env['crm.lead'].search_count(
                    [('partner_id', operator, partner.id)])

        elif self.insurer_type == 1:
            for partner in self:
                proposal = self.env['proposal.opp.bb'].search([('Company', '=', self.id)]).ids
                partner.opp_count = self.env['crm.lead'].search_count(
                    [('proposal_opp','in', proposal)])
        elif self.agent == 1:
            for partner in self:
                operator = 'child_of' if partner.is_company else '='
                partner.opp_count = self.env['crm.lead'].search_count(
                    [('user_id.partner_id', operator, partner.id)])

    @api.multi
    def show_partner_opp(self):
        tree_view = self.env.ref('insurance_broker_system_blackbelts.ibs_crm_case_tree_view_oppor')
        form_view = self.env.ref('insurance_broker_system_blackbelts.crm__lead_form_view')


        if self.customer == 1:
            return {
                'name': ('Opportunity'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.lead',  # model name ?yes true ok
                'views': [(tree_view.id, 'tree'),(form_view.id, 'form')],
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {'default_partner_id': self.id},
                'domain': [('partner_id', '=', self.id)]
            }
        elif self.insurer_type == 1:
            return {
                'name': ('Opportunity'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.lead',  # model name ?yes true ok
                'views': [(tree_view.id, 'tree'),(form_view.id, 'form')],
                'target': 'current',
                'type': 'ir.actions.act_window',
                'domain': [('proposal_opp.Company', '=', self.id)],

            }
        elif self.agent == 1:
            return {
                'name': ('Opportunity'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.lead',  # model name ?yes true ok
                'views': [(tree_view.id, 'tree'),(form_view.id, 'form')],
                'target': 'current',
                'type': 'ir.actions.act_window',
                'domain': [('user_id.partner_id', '=', self.id)],
            }
    # @api.one
    # def _compute_claim_count(self):
    #     if self.customer == 1:
    #         for partner in self:
    #             operator = 'child_of' if partner.is_company else '='
    #             partner.claim_count = self.env['insurance.claim'].search_count(
    #                 [('customer_policy', operator, partner.id)])
    #     elif self.insurer_type == 1:
    #         for partner in self:
    #             operator = 'child_of' if partner.is_company else '='
    #             partner.claim_count = self.env['insurance.claim'].search_count(
    #                 [('insurer', operator, partner.id)])
    #     elif self.agent == 1:
    #         for partner in self:
    #             operator = 'child_of' if partner.is_company else '='
    #             policy = self.env['policy.broker'].search(
    #                 [('salesperson', operator, partner.id)]).ids
    #             partner.claim_count = self.env['insurance.claim'].search_count(
    #                 [('policy_number', operator, policy)])
    #


    # @api.multi
    # def show_partner_claim(self):
    #     if self.customer == 1:
    #         return {
    #             'name': ('Claim'),
    #             'view_type': 'form',
    #             'view_mode': 'tree,form',
    #             'res_model': 'insurance.claim',  # model name ?yes true ok
    #             'target': 'current',
    #             'type': 'ir.actions.act_window',
    #             'context': {'default_customer_policy': self.id},
    #             'domain': [('customer_policy', '=', self.id)]
    #         }
    #     elif self.insurer_type == 1:
    #         return {
    #             'name': ('Claim'),
    #             'view_type': 'form',
    #             'view_mode': 'tree,form',
    #             'res_model': 'insurance.claim',  # model name ?yes true ok
    #             'target': 'current',
    #             'type': 'ir.actions.act_window',
    #             'context': {'default_insurer': self.id},
    #             'domain': [('insurer', '=', self.id)]
    #         }
    #     elif self.agent == 1:
    #         return {
    #             'name': ('Claim'),
    #             'view_type': 'form',
    #             'view_mode': 'tree,form',
    #             'res_model': 'insurance.claim',  # model name ?yes true ok
    #             'target': 'current',
    #             'type': 'ir.actions.act_window',
    #             # 'context': {'default_agent': self.id},
    #             'domain': [('policy_number.salesperson', '=', self.id)]
    #         }

    @api.one
    def _compute_brok_inv_count(self):
        if self.insurer_type == 1:
            for partner in self:
                operator = 'child_of' if partner.is_company else '='
                partner.brok_inv_count= self.env['account.invoice'].search_count(
                    [('partner_id', operator, partner.id),('insured_invoice', '=', 'brokerage')])
    @api.one
    def _compute_prem_bill_count(self):
        if self.insurer_type == 1:
            for partner in self:
                operator = 'child_of' if partner.is_company else '='
                partner.prem_bill_count= self.env['account.invoice'].search_count(
                    [('partner_id', operator, partner.id),('insured_invoice', '=', 'insurer_bill')])

    @api.multi
    def show_brok_inv(self):
        if self.insurer_type == 1:
            return {
                'name': ('Brokerage Invoices'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',  # model name ?yes true ok
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {'default_partner_id': self.id},
                'domain': [('type','=','out_invoice'),('partner_id', '=', self.id),('insured_invoice','=','brokerage')]
            }

    @api.multi
    def show_prem_bill(self):
        if self.insurer_type == 1:
            return {
                'name': ('Premium Bills'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',  # model name ?yes true ok
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {'default_partner_id': self.id},
                'domain': [('partner_id', '=', self.id),('type','=','in_invoice'),('insured_invoice','=','insurer_bill')]
            }

    @api.multi
    def partner_report_opp(self):
        if self.insurer_type:
            proposal = self.env['proposal.opp.bb'].search([('Company', '=', self.id)]).ids
            opp = self.env['crm.lead'].search([('proposal_opp', 'in', proposal)])
            return opp
        elif self.customer:
            opp = self.env['crm.lead'].search([('partner_id', '=', self.id)])
            return opp
        elif self.agent:
            print("***************")
            opp = self.env['crm.lead'].search([('user_id.partner_id', '=', self.id)])
            return opp
    @api.multi
    def partner_report_policy(self):
        if self.insurer_type:
            # proposal = self.env['proposal.opp.bb'].search([('Company', '=', self.id)]).ids
            policy = self.env['policy.broker'].search([('company', '=', self.id)])
            return policy
        elif self.customer:
            # proposal = self.env['proposal.opp.bb'].search([('Company', '=', self.id)]).ids
            policy = self.env['policy.broker'].search([('customer', '=', self.id)])
            return policy
        elif self.agent:
            print("***************")
            policy = self.env['policy.broker'].search([('salesperson', '=', self.id)])
            return policy

    # @api.multi
    # def partner_report_claim(self):
    #     if self.insurer_type:
    #         # proposal = self.env['proposal.opp.bb'].search([('Company', '=', self.id)]).ids
    #         claim = self.env['insurance.claim'].search([('insurer', '=', self.id)])
    #         return claim
    #     elif self.customer:
    #         claim = self.env['insurance.claim'].search([('customer_policy', '=', self.id)])
    #         return claim
    #     elif self.agent:
    #         policy = self.env['policy.broker'].search([('salesperson', '=', self.id)]).ids
    #         claim = self.env['insurance.claim'].search([('policy_number', 'in', policy)])
    #         return claim

# class inhertleaves(models.Model):
#     _inherit = 'hr.holidays'
#
#     @api.model
#     def create(self, values):
#
#         return super(inhertleaves, self).create(values)
