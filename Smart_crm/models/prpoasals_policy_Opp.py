from odoo import api, fields, models
from odoo.exceptions import  ValidationError
from datetime import datetime,timedelta

class Proposals_opp(models.Model):
    _name='proposal.opp.bb'
    _rec_name='proposal_desc'

    proposal_crm = fields.Many2one("crm.lead")
    # proposal_id=fields.Char('ID')
    instype=fields.Selection(related='proposal_crm.insurance_type')
    line=fields.Many2one(related='proposal_crm.LOB',domain="[('insurance_type','=',instype)]")
    Company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer")
    product_pol = fields.Many2one('insurance.product',domain="[('insurer','=',Company),('line_of_bus','=',line)]", string="Product")
    premium = fields.Float('Premium',compute='set_prem',force_save=True)
    test=fields.Char(string='type')
    group = fields.Boolean('Groups')
    proposal_desc=fields.Char('Description',compute="_proposal_desc",store=True)
    # risk_cover_selected= fields.Many2one('risks.opp')
    show_risks_covers=fields.Boolean('')
    # selected_id=fields.Integer('')



    @api.one
    @api.depends('proposal_crm')
    def _proposal_desc(self):
        self.proposal_desc = str(self.Company.name)+" - "+str(self.product_pol.product_name)
    # @api.multi
    # def get_covers(self):
    #     for lead in self:
    #         covers_ids = []
    #         if self.proposal_risks:
    #             for rec in self.proposal_risks:
    #                 covers_ids=self.proposal_risks[0].risks_covers.ids
    #                 for car in self.risk_cover_selected:
    #                     covers_ids = car.risks_covers.ids
    #
    #         lead.selected_risk_covers = [(6,0, covers_ids)]







    #check test?yes
    # @api.multi show me button click
    # @api.onchange("proposals_covers")
    # def _check_preimum_opp(self):
    #     print('iiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    #     for rec in self:
    #         total = 0.0
    #         for reco in rec.proposals_covers:
    #             total += reco.net_perimum
    #
    #         rec.premium = total
    #
    #
    #
    #
    # # @api.multi
    # # @api.onchange("Company", "product_pol")
    # def onchange_num_covers_rel_ids_opp(self):
    #     ids = self.env['insurance.product.coverage'].search([('product_id', '=', self.product_pol.id)])
    #     # print(ids)
    #     res = []
    #     for rec in ids:
    #         res.append((0, 0, {
    #             "name": rec.Name,
    #             "sum_insure": rec.defaultvalue,
    #             "check": rec.readonly,
    #             # "rate": rec.product_id.name_cover_ids.covers_rel_ids.rate,
    #             "net_perimum": rec.readonly and rec.defaultvalue
    #         }))
    #     self.proposals_covers = res


    # @api.multi
    # @api.onchange('Company')
    # def get_risk_proposal(self):
    #     result = []
    #     for risk in self.proposal_crm.objectrisks:
    #         result.append(risk.id)
    #
    #     self.proposal_risks = [(6,0, result)]




    # @api.multi
    # @api.depends('Company')
    # def get_person_proposal(self):
    #     result = []
    #     # import pdb;
    #     # pdb.set_trace()test check for other is it working or not
    #     for person in self.proposal_crm.objectperson:
    #         result.append((0, 0, {
    #             'name': person.name,'DOB': person.DOB, 'job': person.job
    #         }))
    #
    #     self.person_proposal_test = result

    # @api.multi
    # @api.depends('Company')
    # def get_cargo_proposal(self):
    #     result = []
    #     for cargo in self.proposal_crm.objectcargo:
    #         result.append((0, 0, {
    #             'From': cargo.From, 'To': cargo.To, 'cargo_type': cargo.cargo_type, "weight": cargo.weight
    #         }))
    #
    #     self.cargo_proposal_test = result

    select_crm = fields.Many2one('crm.lead')
    # proposal_risks = fields.One2many('risks.opp', 'proposal_risks_opp', force_save=True)

    # car_proposal_test_selected = fields.One2many(related='car')
   # group_proposal = fields.One2many('group.group.opp', 'proposal_group_opp', string='group proposal', readonly=True)


    # @api.constrains('product_pol')
    # @api.multi
    # @api.onchange('product_pol')
    # def _setcovers_veh(self):
    #   if self.product_pol:
    #     print('i enter')
    #     if self.car_proposal_test2:
    #         print('xxx')
    #         for car in self.car_proposal_test2:
    #
    #             rec = self.env['insurance.product.coverage'].search(
    #                 [('product_id', '=', self.product_pol.id)])
    #             import pdb;
    #             pdb.set_trace()
    #
    #             return {'domain': {'car_proposal_test2.covers_car.name': [('id', 'in', rec.ids)]}}
    #




    # @api.constrains('product_pol')
    # @api.onchange('product_pol')
    # def setcovers_person(self):
    #     print('i enter')
    #
    #     if self.person_proposal_risks:
    #         print('xxx')
    #         for person in self.person_proposal_risks:
    #             person.covers_person=False
    #             res = []
    #             ids = self.env['insurance.product.coverage'].search(
    #                 [('product_id', '=', self.product_pol.id)])
    #             # print(ids)
    #             for rec in ids:
    #                 res.append((0, 0, {
    #                     "name": rec.Name,
    #                     "sum_insure": rec.defaultvalue,
    #                     "check": rec.readonly,
    #                     # "rate": rec.product_id.name_cover_ids.covers_rel_ids.rate,
    #                     "net_perimum": rec.readonly and rec.defaultvalue
    #                 }))
    #                 # import pdb;
    #                 # pdb.set_trace()
    #
    #             person.covers_person = res
    #
    # @api.constrains('product_pol')
    # @api.onchange('product_pol')
    # def setcovers_cargo(self):
    #     print('i enter')
    #     if self.cargo_proposal_risks:
    #         print('xxx')
    #         for cargo in self.cargo_proposal_risks:
    #             cargo.covers_cargo=False
    #             res = []
    #             ids = self.env['insurance.product.coverage'].search(
    #                 [('product_id', '=', self.product_pol.id)])
    #             # print(ids)
    #             for rec in ids:
    #                 res.append((0, 0, {
    #                     "name": rec.Name,
    #                     "sum_insure": rec.defaultvalue,
    #                     "check": rec.readonly,
    #                     # "rate": rec.product_id.name_cover_ids.covers_rel_ids.rate,
    #                     "net_perimum": rec.readonly and rec.defaultvalue
    #                 }))
    #                 # import pdb;
    #                 # pdb.set_trace()
    #
    #             cargo.covers_cargo = res

    @api.one
    @api.depends('proposal_crm.coverage_line')
    def set_prem(self):
        if self.proposal_crm.coverage_line:
            print ('mostafa')
            self.premium=0
            for rec in self:
                ids = self.env['coverage.line'].search(
                                [('proposal_id', '=', rec.id)])
                for coverrecord in ids:
                    self.premium+=coverrecord.net_premium

                print (ids)


    def save(self):
        self.show_risks_covers = True
        return True

    @api.onchange('Company')
    def settest(self):
        self.test = self.proposal_crm.test


    @api.onchange('Company')
    def setgroup(self):
        self.group = self.proposal_crm.group

    @api.onchange('Company')
    def setid(self):
        self.rel= self.id
        print(self.rel)

    @api.multi
    def select_proposal(self):
        self.proposal_crm.test1 = True
        self.proposal_crm.prop_id = self.id






