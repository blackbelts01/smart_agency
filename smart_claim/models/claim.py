from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError

class claimPolicy(models.Model):
    _name ="insurance.claim"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Claim Number', required=True, copy=False, index=True)
    intimation_date=fields.Date(string='Intimation Date')
    intimation_no=fields.Char(string='Intimation No')
    dateofloss=fields.Date(string='Date of Loss')
    causeofloss=fields.Many2one('insurance.setup.item',string='Cause of Loss',domain="[('setup_id.setup_key','=','closs')]")
    natureofloss=fields.Many2one('insurance.setup.item',string='Nature of Loss',domain="[('setup_id.setup_key','=','nloss')]")
    lossdesc=fields.Text(string='Loss Desc.')
    naturelossdesc = fields.Text(string='Nature of Loss Desc.')
    typeofgoods = fields.Many2one('insurance.setup.item', string='Type of Goods',domain="[('setup_id.setup_key','=','goods')]")
    remarks=fields.Char(string='Close/Open Remarks')
    totalloss=fields.Boolean(string='Total Loss')
    totalclaimexp=fields.Float(string='Total Claim Expected')
    totalsettled=fields.Float(string='Total Settled',compute='_compute_totalsettled')
    totalunpaid = fields.Float(string='Total Unpaid')

    claimstatus=fields.Many2one('insurance.setup.item',string='Claim Status',domain="[('setup_id.setup_key','=','state')]")
    policy_number = fields.Many2one('policy.broker',string='Policy Number',required=True,domain="[('policy_status','=','approved'),('edit_number','=',0)]")
    endorsement= fields.Many2one('policy.broker',string='Endorsement Number',domain="[('edit_number','!=',0),('std_id','=',related_policy)]")
    related_policy=fields.Char(related='policy_number.std_id',store=True,readonly=True)
    customer_policy=fields.Many2one('res.partner',string='Customer',store=True,readonly=True)
    insured=fields.Char(string='Insured',store=True)
    beneficiary = fields.Char(string='Beneficiary', store=True,readonly=True)
    currency = fields.Many2one('res.currency',string="Currency")
    lob = fields.Many2one('insurance.line.business', string='Line of Business', store=True,readonly=True)
    product = fields.Many2one('insurance.product', string='Product', store=True,readonly=True)
    insurer = fields.Many2one('res.partner', string='Insurer', store=True,readonly=True)
    insurer_branch= fields.Many2one('insurance.setup.item', string='Insurer Branch')
    insurer_contact= fields.Many2one('res.partner',string='Insurer Contact')
    total_paid_amount=fields.Float(string='Total Paid Amount',compute='_compute_payment_history')
    settlement_type=fields.Many2one('insurance.setup.item',string='Settlement Type',domain="[('setup_id.setup_key','=','setltype')]")
    settle_history=fields.One2many('settle.history','claimheader',string='Settle History')
    payment_history=fields.One2many('payment.history','header_payment',string='Payment History')
    claim_action=fields.One2many('product.claim.action','claim',related='product.claim_action')


    @api.multi
    def print_claim(self):
        return self.env.ref('insurance_broker_system_blackbelts.insurance_claim').report_action(self)

    @api.multi
    def send_mail_template_claim(self):
        # Find the e-mail template
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.env.ref('insurance_broker_system_blackbelts.claim_email_template')
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'insurance.claim',
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

    @api.onchange('insurer')
    def _onchange_insurer_branch(self):
      if self.insurer:
           return {'domain': {'insurer_branch': [('setup_id.setup_key','=','branch'),('setup_id.setup_id','=',self.insurer.name)]}}

    @api.onchange('insurer')
    def _onchange_insurer_contact(self):
        if self.insurer:
            return {'domain': {'insurer_contact': [('parent_id','=',self.insurer.id)]}}

    @api.onchange('endorsement','policy_number')
    def _onchange_policy_details(self):
        if self.endorsement:
            self.customer_policy = self.endorsement.customer
            self.insured = self.endorsement.line_of_bussines.object
            self.lob = self.endorsement.line_of_bussines
            self.product = self.endorsement.product_policy
            self.insurer = self.endorsement.company
            self.insurer_branch=self.endorsement.branch.id
            self.beneficiary = self.endorsement.benefit
            self.currency = self.endorsement.currency_id.id

        else:
            self.customer_policy=self.policy_number.customer
            self.insured =self.policy_number.line_of_bussines.object
            self.lob=self.policy_number.line_of_bussines
            self.product=self.policy_number.product_policy
            self.insurer=self.policy_number.company
            self.insurer_branch = self.policy_number.branch.id
            self.beneficiary=self.policy_number.benefit
            self.currency = self.policy_number.currency_id.id

    @api.one
    @api.depends('payment_history')
    def _compute_payment_history(self):
        if self.payment_history:
            self.total_paid_amount = 0.0
            for record in self.payment_history:
                self.total_paid_amount+= record.paid_amount

    @api.onchange('total_paid_amount','totalclaimexp')
    def _onchange_total_unpaid(self):
        if self.total_paid_amount and self.totalclaimexp:
            self.totalunpaid = self.totalclaimexp - self.total_paid_amount


    @api.one
    @api.depends('settle_history')
    def _compute_totalsettled(self):
        if self.settle_history:
            self.totalsettled = 0.0
            for record in self.settle_history:
                self.totalsettled += record.sum_insured


class settleHistory(models.Model):
    _name ="settle.history"

    endorsement_related=fields.Many2one('policy.broker')
    risk_type=fields.Char(related='claimheader.insured',string='Risk Type',readonly=True,store=True)
    risk_id=fields.Many2one('policy.risk',string='Risk',domain="[('policy_risk_id','=',endorsement_related)]")
    risk=fields.Char(related='risk_id.risk_description',string='Risk')
    #Vehicle details
    vcar_type = fields.Many2one(related='risk_id.car_tybe',string='Vehicle Type')
    vmotor_cc = fields.Char(related='risk_id.motor_cc',string="Motor cc")
    vyear_of_made = fields.Char(related='risk_id.year_of_made',string="Year of Made")
    vbrande = fields.Many2one(related='risk_id.Man',string='Maker')
    vmodel = fields.Many2one(related='risk_id.model',string="Model")
    #Person details
    pname = fields.Char(related='risk_id.name',string='Name')
    p_birthday = fields.Date(related='risk_id.DOB',string='Date Of Birth')
    pjob = fields.Many2one(related='risk_id.job',string='Job Type')
    #Cargo details
    cfrom = fields.Char(related='risk_id.From',string='From')
    cto = fields.Char(related='risk_id.To',string='To')
    ctype = fields.Char(related='risk_id.cargo_type',string="Type Of Cargo")
    cweight = fields.Float(related='risk_id.weight',string='Weight')

    coverage = fields.Many2one('covers.lines',string='Coverage',domain="[('policy_rel_id','=',endorsement_related),('riskk', '=',risk_id)]")
    sum_insured=fields.Float(related='coverage.sum_insure',string='Sum Insured',store=True,readonly=True)
    settle_amount=fields.Float(string='Settle Amount',compute='_onchange_settle_amount')
    settle_date=fields.Date(string='Settle Date')
    status=fields.Many2one('insurance.setup.item',string='Status',domain="[('setup_id.setup_key','=','state')]")
    claimheader=fields.Many2one('insurance.claim')
    claim_item=fields.One2many('insurance.claim.item','settle_history',string='Repair/Claim Items')

    @api.onchange('claimheader')
    def _onchange_endo(self):
      if self.claimheader.endorsement:
          self.endorsement_related=self.claimheader.endorsement.id

      else:
          self.endorsement_related = self.claimheader.policy_number.id


    @api.one
    @api.depends('claim_item')
    def _onchange_settle_amount(self):
        if self.claim_item:
            self.settle_amount=0.0
            for record in self.claim_item:
                self.settle_amount += record.amount


class paymentHistory(models.Model):
    _name ="payment.history"

    payment_date=fields.Date(string='Payment Date')
    paid_amount=fields.Float(string='Paid Amount')
    currency=fields.Many2one('res.currency', string="Currency")
    check_bank=fields.Many2one('res.bank',string='Bank')
    check_number=fields.Char(string='Check Number')
    payee=fields.Char(string='Payee Name')
    header_payment=fields.Many2one('insurance.claim')

class claimItem(models.Model):
    _name ="insurance.claim.item"
    _rec_name = "claim_item"

    claim_item=fields.Many2one('insurance.setup.item',string='Items',domain="[('setup_id.setup_key','=','clmitem')]")
    amount=fields.Float(string='Cost')
    settle_history=fields.Many2one('settle.history')






