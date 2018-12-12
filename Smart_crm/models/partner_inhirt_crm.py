from odoo import models, fields, api
from odoo.exceptions import ValidationError



class inhertResPartner(models.Model):
    _inherit = 'res.partner'




    opp_count = fields.Integer(compute='_compute_opp_count')




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
        tree_view = self.env.ref('Smart_crm.ibs_crm_case_tree_view_oppor')
        form_view = self.env.ref('Smart_crm.crm__lead_form_view')


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
    #
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


