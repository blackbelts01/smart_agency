from odoo import models, fields, api
from odoo.exceptions import ValidationError


class policyrisks(models.Model):
    _name="policy.risk"
    _rec_name='risk_description'

    @api.one
    @api.depends('policy_risk_id')
    def _compute_risk_descriptionn(self):
        if  self.policy_risk_id:
            if self.test == "person":
                self.risk_description = "N: "+(str(self.name) +" - " if self.name else " " + "_") + "   " + "DOB: "+(
                    str(self.DOB)+" - " if self.DOB else " " + "_") + "   " +"J : "+ (str(self.job.name) if self.job.name else " " + "_")


            if self.test == "vehicle":
                self.risk_description = "VT: "+(str(self.car_tybe.name)+ ' - ' if self.car_tybe.name else " " + "_") + "   " +"MK: "+ (
                    str(self.Man.setup_id)+ " - " if self.Man.setup_id else " " + "_") + "  " +"MD: "+ (
                                           str(self.model.name)+" - " if self.model.name else " " + "_") + "   " +"YR: "+ (
                                           str(self.year_of_made)+" - " if self.year_of_made else " " + "_") + "  " +"PN: "+ (
                                           str(self.plate_no)+ ' - ' if self.plate_no else " " + "_")+"  "+"CH: "+ (
                                           str(self.chassis_no)+ ' - ' if self.chassis_no else " " + "_")+"  "+"EN: "+ (
                                           str(self.engine)+ ' - ' if self.engine else " " + "_")+"  "+"VCC: "+ (
                                           str(self.motor_cc) if self.motor_cc else " " + "_")
            #
            if self.test == "cargo":
                self.risk_description = "FRM: "+(str(self.From)+" - " if self.From else " " + "_") + "   " + "TO: "+(
                    str(self.To)+" - " if self.To else " " + "_") + "   " +"Typ: "+ (
                                           str(self.cargo_type)+" - " if self.cargo_type else " " + "_") + "   " +"WGT: "+ (
                                           str(self.weight) if self.weight else " " + "_")
            if self.test == "location":
                self.risk_description = "ADD: "+(str(self.address)+" - " if self.address else " " + "_") + "  " +"TYPE: "+ (
                    str(self.type) if self.type else " " + "_")
        else:
            self.risk_descriptio="aya"

            # if rec.test == "location":
            #     rec.risk_description = (str(rec.group_name) if rec.group_name else " " + "_") + "  " + (
            #         str(rec.count) if rec.count else " " + "_")


    old_id= fields.Integer()
    old_id_end = fields.Integer()
    policy_risk_id = fields.Many2one("policy.broker")

    risks_crm = fields.Many2one("crm.lead", string='Risks')
    test = fields.Selection(related="policy_risk_id.check_item")
    risk_description = fields.Char("Risk Description", compute="_compute_risk_descriptionn", store=True)


    #group car
    car_tybe = fields.Many2one('insurance.setup.item',string='Vehicle Type',domain="[('setup_id.setup_key','=','vehicletype')]")
    motor_cc = fields.Char("Motor cc")
    year_of_made = fields.Char("Year of Make")
    plate_no = fields.Char("Plate Number")
    chassis_no = fields.Char("Chassis Number")
    engine = fields.Char("Engine Number")
    Man = fields.Many2one('insurance.setup',string='Maker',domain="[('setup_key','=','man')]")
    model = fields.Many2one('insurance.setup.item',string='Model')

    @api.onchange('Man')
    def _onchange_Man(self):
      if self.Man:
           return {'domain': {'model': [('setup_id.setup_id','=',self.Man.setup_id if self.Man.setup_id else False)]}}






    #group person
    name = fields.Char('Name' ,copy=True)
    DOB = fields.Date('Date Of Birth',copy=True)
    job = fields.Many2one('insurance.setup.item',string='Job Type',domain="[('setup_id.setup_key','=','jobtype')]")




    #group cargo
    From = fields.Char('From')
    To = fields.Char('To')
    cargo_type = fields.Char("Type Of Cargo")
    weight = fields.Float('Weight')

    address = fields.Char('Address')
    type = fields.Char('type')
    # cargo_type = fields.Char("Type Of Cargo")
    # weight = fields.Float('Weight')

    #gropu group
    group_name=fields.Char('Name')

    count=fields.Char('Group Count')

    file = fields.Binary(string='Group Details File')


    # @api.model
    # def create(self,vals):
    #     self.env["policy.broker"].create({"new_risk_ids.risk":self.risk,"new_risk_ids.risk_description":self.risk_description})
    #
    #
    #     return super(New_Risks, self).create(vals)




    # @api.multi
    # def name_get(self):
    #     result = []
    #     for s in self:
    #         name = str(s.risk) + ' , ' + str(s.policy_risk_id.std_id)
    #         result.append((s.id, name))
    #     return result

    _sql_constraints = [
        ('risk_unique', 'unique(policy_risk_id,risk_description)', 'ID already exists!')]


