import random
import string
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class PolicyBroker(models.Model):
    _name = "policy.broker"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    



# #crm module
    @api.model
    def default_get(self, fields):
            res = super(PolicyBroker, self).default_get(fields)
            if self._context.get('active_model') != 'crm.lead':
                return res
            else:

                lead = self.env['crm.lead'].browse(self._context.get('active_id'))

                # recordrisks = self.env['crm.risk'].search([('id', 'in', lead.objectrisks.ids)])
                # print(recordrisks)
                # records_risks = []
                # for rec in recordrisks:
                #     records_risks.append(rec.id)
                # print(records_risks)
                #
                # recordproposal = self.env['proposal.opp.bb'].search([('id', '=', lead.selected_coverage.id)])
                # print(recordproposal.id)
                # recordcovers = self.env['coverage.line'].search([('proposal_id', '=', recordproposal.id)])
                #
                # records_covers = []
                # for rec in recordcovers:
                #     coversline = (
                #         0, 0,
                #         {'riskk': rec.risk_id_covers.id ,'insurerd': rec.insurer.id,
                #          'prod_product': rec.product.id, 'name1': rec.covers.id, 'sum_insure': rec.sum_insured,
                #          'deductible' : rec.deductible, 'limitone' :rec.limitone ,'limittotal': rec.limittotal ,
                #          'net_perimum': rec.net_premium, 'rate': rec.rate})
                #     print(coversline)
                #     records_covers.append(coversline)
                #     print(records_covers)

                # res['new_risk_ids'] = [(6, 0, records_risks)]
                res['insurance_type'] = lead.insurance_type
                res['line_of_bussines'] = lead.LOB.id
                res['ins_type'] = lead.ins_type
                # res['propoasl_ids'] = records_proposal
                res['customer'] = lead.partner_id.id
                res['salesperson'] = lead.user_id.partner_id.id
                res['std_id'] = lead.policy_number
                # res['name_cover_rel_ids'] = records_covers
                # res['checho'] = True
                res['company'] = lead.selected_coverage.Company.id
                res['product_policy'] = lead.selected_coverage.product_pol.id
                print(self.new_risk_ids)



                return res

    @api.multi
    def send_mail_template_policy(self):
        # Find the e-mail template
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.env.ref('smart_policy.policy_email_template')
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'policy.broker',
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
    @api.onchange("t_permimum","term")
    def _cmpute_date_and_amount(self):
        if self.term == "onetime":
            self.rella_installment_id = [(0, 0, {
                "date": self.start_date,
                "amount": self.t_permimum,
            })]
        elif self.term == "year":
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=365)

            phone_numbers = []
            for i in range(int(self.no_years)):
                x = (0, 0, {
                    "date": start + duration,
                    "amount": self.t_permimum / 1

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=365)
            self.rella_installment_id = phone_numbers
        elif self.term == "quarter":
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=90)
            phone_numbers = []
            for i in range(4):
                x = (0, 0, {
                    "date": start + duration,
                    "amount": self.t_permimum / 4

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=90)
            self.rella_installment_id = phone_numbers
        elif self.term == "month":
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=30)
            phone_numbers = []
            for i in range(12):
                x = (0, 0, {
                    "date": start + duration,
                    "amount": self.t_permimum / 12

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=30)
            self.rella_installment_id = phone_numbers


    @api.onchange('line_of_bussines')
    def _compute_comment_policy(self):
        self.check_item = self.line_of_bussines.object

    @api.multi
    def print_policy(self):
        return self.env.ref('smart_policy.policy_report').report_action(self)

    @api.model
    def compute_date(self):
        if (datetime.today().strftime('%Y-%m-%d')):
            if (datetime.today().strftime('%Y-%m-%d')) >= self.end_date:
                self.renewal_state=True


    bool = fields.Boolean()
    edit_number = fields.Integer(string="Endorsement No.",copy=True)
    edit_decr = fields.Text('Endorsement Description', readonly=True,copy=True)
    last_policy=fields.Many2one('policy.broker')
    policy_number = fields.Char(string="Renewal Policy Number",copy=True)
    renwal_check = fields.Boolean(string="Renewal")
    std_id = fields.Char(string="Policy Number" ,required=True,copy=True)
    issue_date = fields.Date(string="Issue Date",required=True,copy=True)
    start_date = fields.Date(string="Effective From",required=True,copy=True)
    end_date = fields.Date(string="Effective To",required=True,copy=True)
    term = fields.Selection(
        [("onetime", "One Time"), ("year", "yearly"), ("quarter", "Quarterly"), ("month", "Monthly")],
        string="Payment Frequency",copy=True)
    no_years = fields.Integer(string="No. Years", default=1,copy=True)
    gross_perimum = fields.Float(string="Gross Perimum",copy=True)
    t_permimum = fields.Float(string="Net Permium", compute="_compute_t_premium",copy=True)
    salesperson = fields.Many2one('res.partner', string='Salesperson' ,domain="[('agent','=',1)]",copy=True)
    commission_per = fields.Float(string="Commission",compute="_compute_commission_per",copy=True)
    share_commission=fields.One2many('insurance.share.commission','policy_id',string='Share Commissions',copy=True)

    @api.multi
    def _compute_commission_per(self):
        self.commission_per=(self.product_policy.commission_per/100)*self.t_permimum


    @api.onchange("t_permimum","term")
    def onchange_share_commission(self):
        if self.salesperson:
            self.share_commission =[(0, 0, {
                                        'agent': self.salesperson.id,
                                        'commission_per':100,})]



    rella_installment_id = fields.One2many("installment.installment", "installment_rel_id")
    customer = fields.Many2one('res.partner', 'Customer',copy=True)
    insurance_type = fields.Selection([('Life', 'Life'),
                                       ('P&C', 'P&C'),
                                       ('Health', 'Health'), ],
                                      'Insurance Type', track_visibility='onchange',copy=True)
    ins_type = fields.Selection([('Individual', 'Individual'),
                                 ('Group', 'Group'), ],
                                'I&G', track_visibility='onchange',copy=True)
    line_of_bussines = fields.Many2one('insurance.line.business', string='Line of business',
                                       domain="[('insurance_type','=',insurance_type)]",copy=True)
    check_item = fields.Selection(related="line_of_bussines.object",copy=True)
    group = fields.Boolean()
    commision = fields.Float(string="Basic Brokerage", compute="_compute_brokerage",copy=True)
    com_commision = fields.Float(string="Complementary  Brokerage", compute="_compute_brokerage",copy=True)
    fixed_commision = fields.Float(string="Fixed Brokerage", compute="_compute_brokerage",copy=True)
    earl_commision = fields.Float(string="Early Collection" , compute="_compute_brokerage",copy=True)
    total_commision = fields.Float(string="total Brokerage", compute="_compute_brokerage",copy=True)
    new_risk_ids = fields.One2many("policy.risk",'policy_risk_id', string='Risk',copy=True)
    company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer",copy=True)
    product_policy = fields.Many2one('insurance.product',domain="[('insurer','=',company),('line_of_bus','=',line_of_bussines)]", string="Product",copy=True)
    name_cover_rel_ids = fields.One2many("covers.lines","policy_rel_id",string="Covers Details",copy=True)
    currency_id = fields.Many2one("res.currency","Currency Code",copy=True)
    benefit =fields.Char("Beneficiary",copy=True)
    checho = fields.Boolean()
    validate=fields.Selection([('info', 'Info'),
                                ('risk', 'Risk'),
                                ('cover', 'Cover'),
                                ('com', 'Com'),
                                ('bro', 'Bro'),
                                ('ins', 'Ins'),
                                ('inv', 'Inv'),],
                                      'validate', track_visibility='onchange',default='info')


    @api.multi
    def validate_basic(self):
        self.validate = 'info'

    @api.multi
    def validate_risk(self):
        if self.line_of_bussines:
            self.validate = 'risk'
            return True


    @api.multi
    def validate_cover(self):
        if self.new_risk_ids:
            self.validate = 'cover'
            if self.renwal_check:
                coverlines = self.env["covers.lines"].search([('id', 'in', self.name_cover_rel_ids.ids)])
                for rec in coverlines:
                    risk_id = self.env["policy.risk"].search([('old_id', '=', rec.old_risk_id)]).id
                    rec.write({'riskk': risk_id, })
            if self.edit_number:
                coverlines = self.env["covers.lines"].search([('id', 'in', self.name_cover_rel_ids.ids)])
                for rec in coverlines:
                    risk_id = self.env["policy.risk"].search([('old_id_end', '=', rec.old_risk_id_end)]).id
                    rec.write({'riskk': risk_id, })
            return True


    @api.multi
    def validate_commission(self):
        self.validate = 'com'

    @api.multi
    def validate_brokrage(self):
        self.validate = 'bro'

    @api.multi
    def validate_installment(self):
        self.validate = 'ins'

    @api.multi
    def validate_invoice(self):
        self.validate = 'inv'


    @api.onchange('company')
    def _onchange_branch(self):
      if self.company:
           return {'domain': {'branch': [('setup_id.setup_key','=','branch'),('setup_id.setup_id','=',self.company.name)]}}

    branch = fields.Many2one('insurance.setup.item',string="Branch",domain="[('setup_id.setup_key','=','branch'),('setup_id.setup_id','=',company)]",copy=True)



    @api.one
    @api.depends("name_cover_rel_ids")
    def _compute_t_premium(self):
        total = 0.0
        for rec in self:
            for line in rec.name_cover_rel_ids:
                total += line.net_perimum
        rec.t_permimum = total


    @api.multi
    @api.depends("product_policy")
    def _compute_brokerage(self):
        for rec in self:
            rec.commision = (rec.product_policy.brokerage.basic_commission * rec.t_permimum) / 100
            rec.com_commision = (rec.product_policy.brokerage.complementary_commission * rec.t_permimum) / 100
            rec.earl_commision = (rec.product_policy.brokerage.early_collection * rec.t_permimum) / 100
            rec.fixed_commision = (rec.product_policy.brokerage.fixed_commission * rec.t_permimum) / 100
            rec.total_commision = rec.commision + rec.com_commision + rec.fixed_commision + rec.earl_commision

    @api.multi
    def generate_covers(self):
        self.checho = True
        return True
    policy_status = fields.Selection([('pending', 'Pending'),
                                      ('approved', 'Approved'), ],
                                     'Status', required=True, default='pending')
    hide_inv_button = fields.Boolean(copy=False)
    # invoice_ids = fields.One2many('account.invoice', 'insurance_id', string='Invoices', readonly=True)
    renewal_state=fields.Boolean(copy=False,compute='compute_date')
    _sql_constraints = [
        ('std_id_unique', 'unique(std_id,policy_number)', 'Policy Number  already exists!')]



    @api.multi
    def name_get(self):
        result = []
        for s in self:
            name = s.std_id + ' , ' +str(s.edit_number)
            result.append((s.id, name))
        return result

    @api.multi
    def confirm_policy(self):
        if self.term and self.customer and self.line_of_bussines and self.company:
            self.policy_status = 'approved'
            self.hide_inv_button = True
        else:
            raise UserError(_("Customer ,Line of Bussines , Company or Payment Frequency  should be Selected"))


#accounting module
    # @api.multi
    # def create_invoices(self):
    #     for record in self.rella_installment_id:
    #         if record.amount !=0:
    #             cust_invoice=self.env['account.invoice'].create({
    #                 'type': 'out_invoice',
    #                 'partner_id': self.customer.id,
    #                 'insured_invoice': 'customer_invoice',
    #                 'name': 'Customer Invoice from ' +str(self.customer.name),
    #                 'user_id': self.env.user.id,
    #                 'insurance_id': self.id,
    #                 'origin': self.policy_number,
    #                 'insured_type':self.insurance_type,
    #                 'insured_lOB': self.line_of_bussines.id,
    #                 'insured_insurer': self.company.id,
    #                 'insured_product': self.product_policy.id,
    #                 'date_due':record.date,
    #                 'invoice_line_ids': [(0, 0, {
    #                     'name': str(self.line_of_bussines.line_of_business),
    #                     'quantity': 1,
    #                     'price_unit': record.amount,
    #                     'account_id': self.line_of_bussines.income_account.id,
    #                 })],
    #             })
    #             cust_invoice.action_invoice_open()
    # 
    #             ins_bill=self.env['account.invoice'].create({
    #                 'type': 'in_invoice',
    #                 'partner_id': self.company.id,
    #                 'insured_invoice': 'insurer_bill',
    #                 'name': 'Insurer Bill for ' +str(self.company.name),
    #                 'user_id': self.env.user.id,
    #                 'insurance_id': self.id,
    #                 'origin': self.policy_number,
    #                 'insured_type':self.insurance_type,
    #                 'insured_lOB': self.line_of_bussines.id,
    #                 'insured_insurer': self.company.id,
    #                 'insured_product': self.product_policy.id,
    #                 'date_due': record.date,
    #                 'invoice_line_ids': [(0, 0, {
    #                     'name': str(self.line_of_bussines.line_of_business),
    #                     'quantity': 1,
    #                     'price_unit': record.amount,
    #                     'account_id': self.line_of_bussines.expense_account.id,
    #                 })],
    #             })
    #             ins_bill.action_invoice_open()
    # 
    #         if self.total_commision != 0:
    #             brok_invoice = self.env['account.invoice'].create({
    #                 'type': 'out_invoice',
    #                 'partner_id': self.company.id,
    #                 'insured_invoice': 'brokerage',
    #                 'name': 'Brokerage  for ' + str(self.company.name),
    #                 'user_id': self.env.user.id,
    #                 'insurance_id': self.id,
    #                 'origin': self.policy_number,
    #                 'insured_type': self.insurance_type,
    #                 'insured_lOB': self.line_of_bussines.id,
    #                 'insured_insurer': self.company.id,
    #                 'insured_product': self.product_policy.id,
    #                 'date_due': record.date,
    #                 'invoice_line_ids': [(0, 0, {
    #                     'name': str(self.line_of_bussines.line_of_business),
    #                     'quantity': 1,
    #                     'price_unit': self.total_commision,
    #                     'account_id': self.line_of_bussines.income_account.id,
    #                 })],
    #             })
    #             brok_invoice.action_invoice_open()
    # 
    #         for com in self.share_commission:
    #             com_bill = self.env['account.invoice'].create({
    #                 'type': 'in_invoice',
    #                 'partner_id': com.agent.id,
    #                 'insured_invoice': 'commission',
    #                 'name': 'Commission for ' + str(com.agent.name),
    #                 'user_id': self.env.user.id,
    #                 'insurance_id': self.id,
    #                 'origin': self.policy_number,
    #                 'insured_type': self.insurance_type,
    #                 'insured_lOB': self.line_of_bussines.id,
    #                 'insured_insurer': self.company.id,
    #                 'insured_product': self.product_policy.id,
    #                 'date_due': record.date,
    #                 'invoice_line_ids': [(0, 0, {
    #                     'name': str(self.line_of_bussines.line_of_business),
    #                     'quantity': 1,
    #                     'price_unit': com.amount,
    #                     'account_id': self.line_of_bussines.expense_account.id,
    #                 })],
    #             })
    #             com_bill.action_invoice_open()



        # self.hide_inv_button = False

# class AccountInvoiceRelate(models.Model):
#     _inherit = 'account.invoice'
# 
#     insurance_id = fields.Many2one('policy.broker', string='Insurance')
#     insured_type =fields.Char(string='Type')
#     insured_lOB = fields.Many2one('insurance.line.business',string='LOB')
#     insured_insurer = fields.Many2one('res.partner',string='Insurer')
#     insured_product = fields.Many2one('insurance.product',string='Product')
#     insured_invoice=fields.Char(string='insured invoice')


class Extra_Covers(models.Model):
    _name = "covers.lines"
    _rec_name= 'name1'

    riskk = fields.Many2one("policy.risk", "Risk",domain="[('id','in',new_risk_ids)]")

    old_risk_id = fields.Integer()
    old_risk_id_end = fields.Integer()

    insurerd = fields.Many2one(related="policy_rel_id.company")
    prod_product = fields.Many2one(related="policy_rel_id.product_policy",domain="[('insurer','=',insurerd)]")
    name1 = fields.Many2one("insurance.product.coverage",string="Cover", domain="[('product_id', '=' , prod_product)]")
    check = fields.Boolean(related="name1.readonly")
    sum_insure = fields.Float(string="SI")
    deductible = fields.Integer('Deductible')
    limitone=fields.Integer('Limit in One')
    limittotal=fields.Integer('Limit in Total')
    rate = fields.Float(string="Rate")
    net_perimum = fields.Float(string="Net Perimum")
    policy_rel_id = fields.Many2one("policy.broker")
    new_risk_ids =fields.One2many(related='policy_rel_id.new_risk_ids')



    _sql_constraints = [
        ('cover_unique', 'unique(policy_rel_id,riskk,name1)', 'Cover already exists!')]



    @api.onchange("check")
    def _nameget(self):
        if self.check == True:
            self.net_perimum = self.sum_insure



    @api.onchange('name1')
    def onchange_covers(self):
        if self.name1:
            self.sum_insure = self.name1.defaultvalue
            self.deductible = self.name1.deductible
            self.limitone = self.name1.limitone
            self.limittotal = self.name1.limittotal

    @api.onchange('rate','sum_insure')
    def compute_premium(self):
        if self.name1:
            self.net_perimum = (self.sum_insure * self.rate) / 100

    @api.onchange('riskk')
    def onchange_risc_desc(self):
        if self.riskk:
            self.risk_description = self.riskk.risk_description

class ShareCommition(models.Model):
    _name = "insurance.share.commission"
    
    agent = fields.Many2one("res.partner", string="Agent")
    commission_per = fields.Float(string="Percentage")
    amount = fields.Float(string="Amount",compute='_compute_amount')
    policy_id = fields.Many2one("policy.broker")

    @api.one
    @api.depends('commission_per')
    def _compute_amount(self):
        self.amount=self.policy_id.commission_per*(self.commission_per/100)







class InstallmentClass(models.Model):
    _name= "installment.installment"
    _rec_name = "date"

    date = fields.Date(string="Date")
    insurer=fields.Many2one(related="installment_rel_id.company")
    ins_product = fields.Many2one(related="installment_rel_id.product_policy",domain="[('insurer','=',insurer)]")
    policy_number=fields.Char(related='installment_rel_id.std_id')
    ins_type=fields.Selection(related='installment_rel_id.insurance_type')
    lob=fields.Many2one(related='installment_rel_id.line_of_bussines', domain="[('insurance_type','=',ins_type)]")

    customer=fields.Many2one(related='installment_rel_id.customer',string='Customer')
    pay_customer=fields.Boolean(string='Customer Payment')
    pay_date=fields.Date(string='Collection Date')
    pay_method = fields.Many2one('account.journal',string='Collection Method')
    method_type=fields.Selection(related='pay_method.type')
    check_details=fields.Char('Check Details')
    recp_No = fields.Char('Receipt Number')

    delv_insurer = fields.Boolean(string='Delivered')
    delv_date_ins = fields.Date(string='Delivery Date')
    delv_method_ins =fields.Many2one('account.journal',string='Delivery Method')
    check_details_delv=fields.Char('Check Details')
    recp_No_delv = fields.Char('Receipt Number')


    # pay_method_ins = fields.Many2one('account.journal', string='Collection Date')
    customer_pay_check=fields.Boolean(string='Customer Payment',compute='customer_check_payment',store=True)
    insurer_delv_check = fields.Boolean(string='Insurer Delivery',compute='ins_check_delivery',store=True)

    # enddate = fields.Date(string="End of premium")
    amount = fields.Float(string="Amount")
    state = fields.Selection([('open', 'Open'),
                             ('paid', 'Paid')],
                           'State',defualt='open')
    installment_rel_id = fields.Many2one("policy.broker")

    @api.one
    @api.depends('pay_customer')
    def customer_check_payment(self):
        if self.pay_customer:
            self.customer_pay_check=True
    @api.one
    @api.depends('delv_insurer')
    def ins_check_delivery(self):
        if self.delv_insurer:
            self.insurer_delv_check = True






