from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Policy_Info(models.Model):
    _name ="insurance.line.business"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'line_of_business'

    insurance_type = fields.Selection([('Life', 'Life'),
                                       ('P&C', 'P&C'),
                                       ('Health', 'Health'), ],
                                      'Insured Type', track_visibility='onchange', required=True)
    line_of_business = fields.Char(string='Line of Business', required=True)
    object= fields.Selection([('person', 'Person'),
                              ('vehicle', 'Vehicle'),
                              ('cargo', 'Cargo'),
                              ('location', 'Location'),],
                             'Insured Object', track_visibility='onchange', required=True)
    desc = fields.Char(string='Description')
    income_account=fields.Many2one('account.account','Income Account',required=True)
    expense_account = fields.Many2one('account.account','Expense Account',required=True)

    _sql_constraints = [
        ('business_unique', 'unique(insurance_type,line_of_business,object)', 'Line of Business already exists!')]


class Product(models.Model):
    _name='insurance.product'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_name'

    product_name=fields.Char('Product Name',required=True)
    insurer=fields.Many2one('res.partner', string="Insurer",domain="[('insurer_type','=',1)]")
    line_of_bus=fields.Many2one('insurance.line.business','Line of Business')
    coverage=fields.One2many('insurance.product.coverage','product_id',string='Coverage')
    brokerage=fields.One2many('insurance.product.brokerage','product_id',string='Brokerage')
    commission_per=fields.Float(string='Commission Percentage')
    claim_action=fields.One2many('product.claim.action','product')
    name_cover_id = fields.Many2one("name.cover")

    _sql_constraints = [
        ('product_unique', 'unique(product_name,line_of_bus)', 'Product already exists!')]

class claimAction(models.Model):
    _name='product.claim.action'

    action=fields.Char('Claim Action')
    comments=fields.Text(string='Comments')
    product=fields.Many2one('insurance.product')
    # claim=fields.Many2one('insurance.claim')




class coverage(models.Model):
    _name='insurance.product.coverage'
    _rec_name= "Name"

    Name=fields.Char('Cover Name')
    defaultvalue=fields.Float('Default Sum Insured')
    required=fields.Boolean('Required')
    deductible = fields.Float('Deductible')
    limitone=fields.Float('Limit in One')
    limittotal=fields.Float('Limit in Total')
    readonly=fields.Boolean('Read Only')
    product_id=fields.Many2one('insurance.product')
    lop_id=fields.Many2one('insurance.line.business',string='Line of Business')

    _sql_constraints = [
        ('Name_unique', 'unique(Name)', 'Cover Name already exists!')]



class Brokerage(models.Model):
    _name='insurance.product.brokerage'

    datefrom=fields.Date('Date from')
    dateto=fields.Date('Date to')
    basic_commission = fields.Float('Basic Commission')
    complementary_commission = fields.Float('Complementary Commission')
    early_collection = fields.Float('Early Collection Commission')
    fixed_commission = fields.Monetary(default=0.0, currency_field='company_currency_id',string='Fixed Commission')
    company_currency_id = fields.Many2one('res.currency', related='product_id.insurer.currency_id', string="Company Currency", readonly=True,store=True)
    product_id = fields.Many2one('insurance.product')

    @api.constrains('datefrom')
    def _constrain_date(self):
        for record in self:
            if record.dateto < record.datefrom:
                raise ValidationError('Error! Date to Should be After Date from')




class insuranceSetup(models.Model):
    _name = 'insurance.setup'
    _rec_name='setup_id'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    setup_key=fields.Selection([('closs', 'CLOSS'),
                                ('nloss', 'NLOSS'),
                                ('goods', 'GOODS'),
                                ('setltype', 'SETTYPE'),
                                ('state', 'STATE'),
                                ('clmitem', 'CLMITEM'),
                                ('branch', 'INSBRANCH'),
                                ('vehicletype', 'VEHICLETYPE'),
                                ('industry', 'INDUSTRY'),
                                ('man', 'MAKER'),
                                ('jobtype', 'JOBTYPE'),],
                               'KEY', track_visibility='onchange', required=True)
    setup_id=fields.Char(string='ID')
    setup_item=fields.One2many('insurance.setup.item','setup_id',string='List Items')

    @api.onchange('setup_key')
    def _onchange_id(self):
        if self.setup_key:
            self.setup_id= (self.setup_key).upper()


    _sql_constraints = [
        ('setup_id_unique', 'unique(setup_key,setup_id)', 'ID already exists!')]

class insuranceSetupItem(models.Model):
    _name = 'insurance.setup.item'

    name=fields.Char('Item')
    setup_id=fields.Many2one('insurance.setup')

    _sql_constraints = [
        ('item_unique', 'unique(setup_id,name)', 'Item already exists!')]




