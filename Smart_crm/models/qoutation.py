from odoo import models, fields, api
from odoo.exceptions import  ValidationError


class crm_leads(models.Model):
    _inherit = "crm.lead"

    planned_revenue = fields.Float('Expected Premium in Company Currency', track_visibility='always')
    c_type = fields.Many2one('res.currency', string='Expected Premium in Currency')
    ammount = fields.Float(string='Ammount')
    # user_id = fields.Many2one('res.users', string='Lead Operator', index=True, track_visibility='onchange',
    #                           default=lambda self: self.env.user )
    create_uid = fields.Many2one('res.users', string='Lead Generator')
    policy_number = fields.Char( string='Policy Number')

    insurance_type = fields.Selection([('Life', 'Life'),
                                       ('P&C', 'P&C'),
                                       ('Health', 'Health'), ],
                                      'Insurance Type', track_visibility='onchange',required=True)
    ins_type = fields.Selection([('Individual', 'Individual'),
                                 ('Group', 'Group'),],
                                'insured type', track_visibility='onchange')
    duration_no = fields.Integer('Policy Duration Number')
    duration_type =fields.Selection([('day', 'Day'),
                                     ('month', 'Month'),
                                     ('year', 'Year'),],
                                    'Policy Duration Type',track_visibility='onchange')
    term=fields.Char(string='Term',compute='_compute_term',force_save=True)

    validate_basic_mark_opp = fields.Boolean(copy=False, default=True)
    validate_risk_mark_opp = fields.Boolean(copy=False)
    validate_prop = fields.Boolean(copy=False)
    validate_prop_line = fields.Boolean(copy=False)
    validate_underwr=fields.Boolean(copy=False)
    validate_contact = fields.Boolean(copy=False)

    @api.multi
    def validate_basic_opp(self):
        self.validate_basic_mark_opp = True
        self.validate_risk_mark_opp = False
        self.validate_prop = False
        self.validate_prop_line = False
        self.validate_underwr = False
        self.validate_contact = False
        print(self.validate_basic_mark_opp)

        return True

    @api.multi
    def validate_risk_opp(self):
        if self.LOB:
            self.validate_basic_mark_opp = False
            self.validate_risk_mark_opp = True
            self.validate_prop = False
            self.validate_prop_line = False
            self.validate_underwr = False
            self.validate_contact = False
            print(self.validate_basic_mark_opp)
            return True

    @api.multi
    def validate_proposal(self):
        if self.objectrisks:
            self.validate_basic_mark_opp = False
            self.validate_risk_mark_opp = False
            self.validate_prop = True
            self.validate_prop_line = False
            self.validate_underwr = False
            self.validate_contact = False
            return True
    @api.multi
    def validate_proposal_line(self):
        if self.objectrisks and self.proposal_opp:
            self.validate_basic_mark_opp = False
            self.validate_risk_mark_opp = False
            self.validate_prop = False
            self.validate_prop_line = True
            self.validate_underwr = False
            self.validate_contact = False
            return True

    @api.multi
    def validate_underwritting(self):
                self.validate_basic_mark_opp = False
                self.validate_risk_mark_opp = False
                self.validate_prop = False
                self.validate_prop_line = False
                self.validate_underwr=True
                self.validate_contact = False


    @api.multi
    def validate_continfo(self):
        self.validate_basic_mark_opp = False
        self.validate_risk_mark_opp = False
        self.validate_prop = False
        self.validate_prop_line = False
        self.validate_underwr = False
        self.validate_contact = True


    @api.one
    def _compute_term(self):
        if self.duration_no and self.duration_type:
            self.term = str(self.duration_no) + '-' + str(self.duration_type)

    LOB = fields.Many2one('insurance.line.business', string='Line of business', domain="[('insurance_type','=',insurance_type)]",required=True)

    oppor_type = fields.Char(
        string='Opportunity type',
        compute='_changeopp',
        store=False,
        compute_sudo=True,
    )







    #pol=fields.Many2one(related='Policy_type.insured_type' , string='insured type')
    test=fields.Char('')
    group=fields.Boolean('Groups')
    individual = fields.Boolean('Item by Item')
    test1=fields.Boolean(readonly=True)

    objectrisks = fields.One2many('crm.risk', 'risks_crm', string='car',copy=True)  # where you are using this fiedl ? in xml

    # objectgroup = fields.One2many('group.group.opp', 'object_group_crm', string='Group')

    proposal_opp = fields.One2many('proposal.opp.bb', 'proposal_crm', string='proposla')

    coverage_line = fields.One2many('coverage.line', 'covers_crm', 'Coverage lines')

    selected_proposal = fields.One2many('proposal.opp.bb', 'select_crm', compute='proposalselected')
    prop_id = fields.Integer('', readonly=True)
    my_notes = fields.Text('Under writting')

    # covers=fields.One2many(related='selected_proposal.proposals_covers')

    # policy_opp=fields.Many2one('policy.broker')
    selected_coverage = fields.Many2one('proposal.opp.bb', domain="[('proposal_crm','=',id)]",string='Final Proposal')
    set_covers = fields.Boolean('')
    test_computed = fields.Char('', compute='testcom')
    @api.depends('ins_type')
    def testcom(self):
        self.test_computed='Islam'








    def proposalselected(self):
        print('5555555')
        ids = self.env['proposal.opp.bb'].search([('id', '=',self.prop_id)]).ids
        self.selected_proposal = [(6, 0, ids)]

    @api.multi
    def covers_button(self):
        self.set_covers=True
        # self.coverage_line.covers_crm=self.id
        return True
        # form_view = self.env.ref('insurance_broker_system_blackbelts.Risks_form')

        # return {
        #     'name': ('Risk Details'),
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'views': [(form_view.id, 'form')],
        #     'res_model': 'risks.opp',
        #     'target': 'inline',
        #     'type': 'ir.actions.act_window',
        #     'context': {'default_risks_crm': self.id},
        #     'flags': {'form': {'action_buttons': True}}


    @api.multi
    def proposal_button(self):
        form_view = self.env.ref('insurance_broker_system_blackbelts.form_proposal_opp')

        return {
            'name': ('Proposals'),
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(form_view.id, 'form')],
            'res_model': 'proposal.opp.bb',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {'default_proposal_crm':self.id},
        }


    # objectcar_selected = fields.Many2one('car.object', string='car')
    # objectperson_selected = fields.Many2one('person.object', string='Person')
    # objectcargo_selected = fields.Many2one('cargo.object', string='cargo')
    # objectgroup_selected = fields.Many2one('group.group', string='Group')





    # @api.onchange('user_id')
    # def get_car_proposal_crm(self):
    #     for lead in self:
    #         proposal_ids = []
    #         for car in self.objectcar:
    #             if car.btn1:
    #                 proposal_ids = proposal_ids+car.proposal_car.ids
    #         lead.prop_car = [(6,0, proposal_ids)]



    # @api.multi
    # def button_action(self):
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': 'http://167.99.243.240/moodle/login/index.php?username=%{0}&password=Admin%40123&Submit=Login' .format(self.env.user.name),
    #         'target': 'self',
    #         'res_id': self.id,
    #     }



    #prop_car=fields.One2many(related='objectcar')
    # prop_person = fields.One2many(related='objectperson_selected.proposal_person')
    # prop_cargo = fields.One2many(related='objectcargo_selected.proposal_cargo')
    # prop_group = fields.One2many(related='objectgroup_selected.proposal_group')

    @api.multi
    def create_policy(self):
        form_view = self.env.ref('smart_policy.policy_form_view')
        if self.policy_number and self.selected_coverage:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(form_view.id, 'form')],
                'res_model': 'policy.broker',
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {},
            }
        else:
            raise ValidationError(
                ('You Must Enter the Policy Number '
                 'OR select final proposal  .'))

            # , 'default_objectperson':records_person ,'default_objectcar':records_car},

        # #  tree and form view id here.
        # proposal_car_tree  form_proposal
        # view = self.env.ref('crm__black_belts.proposal_car_tree')
        # form_view = self.env.ref('insurance_broker_blackbelts.my_view_for_policy_form_kmlo1')
        # print(self.objectperson.ids)
        #
        # #self.policy_opp.test=self.test
        # return {
        #     'name': 'Policy',
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': ' form',
        #     'views': [(form_view.id, 'form')],
        #     'res_model': 'policy.broker',
        #     'target': 'current',
        #     'context': {'default_policy_opp':self,'default_insurance_type': self.insurance_type, 'default_line_of_bussines': self.LOB.id,
        #                 'default_ins_type': self.ins_type
        #         , 'default_objectvehicle': self.objectcar.ids, 'default_objectperson':  self.objectperson.ids},
        #
        #
        #
        #
        # }





    @api.onchange('LOB')
    def _compute_comment(self):
        for record in self:
            record.test = record.LOB.object
            print (record.test)






    #@api.onchange('user_id')
    #def onchange_user_id(self):
    #   if self.user_id and self.env.uid != 1 :
    #        return {'domain':{'user_id': [('id','in',[self.env.uid,1])]}}


    @api.onchange('user_id', 'create_uid')
    def _changeopp(self):
        for record in self:
            if record.create_uid:
                if record.create_uid == record.user_id:
                    record['oppor_type'] = 'Own'

                else:
                    record['oppor_type'] = 'Network'
            else :
                record.create_uid=self.env.uid

    @api.multi
    def print_opp(self):
        return self.env.ref('insurance_broker_system_blackbelts.crm_report').report_action(self)

    @api.multi
    def send_mail_template(self):
        # Find the e-mail template
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.env.ref('insurance_broker_system_blackbelts.opp_email_template')
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'crm.lead',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id.id),
            'default_template_id': template_id.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            # 'custom_layout': "sale.mail_template_data_notification_email_sale_order",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True
        }

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        # You can also find the e-mail template like this:
        # template = self.env['ir.model.data'].get_object('mail_template_demo', 'example_email_template')

        # Send out the e-mail template to the user
        template_id.send_mail(self.ids[0], force_send=True)
        # self.env['mail.template'].browse(template.id).send_mail(self.id)





    @api.onchange('ammount', 'c_type')
    def _change(self):
        if self.c_type.id:
            self.planned_revenue = self.ammount / self.c_type.rate
            print(self.c_type.rate)




class crm_leads_currency(models.Model):
    _inherit = 'res.currency'
    # currency_type=fields.One2many('crm.lead','currency_type ',string='currency')
    c = fields.One2many('crm.lead', 'c_type', string='currency')














