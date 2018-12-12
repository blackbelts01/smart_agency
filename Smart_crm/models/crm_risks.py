from odoo import models, fields, api
from odoo.exceptions import ValidationError


class New_Risks(models.Model):
    _name='crm.risk'
    _inherit = "policy.risk"
    # _rec_name='risk_description'


    @api.one

    @api.depends('risks_crm')
    def _compute_risk_description_crm(self):
        if self.risks_crm :
            if self.type_risk == 'person':
                self.risk_description = "N: "+(str(self.name) +" - " if self.name else " " + "_") + "   " + "DOB: "+(
                    str(self.DOB)+" - " if self.DOB else " " + "_") + "   " +"J : "+ (str(self.job.name) if self.job.name else " " + "_")


            if  self.type_risk == 'vehicle':
                self.risk_description = "VT: "+(str(self.car_tybe.name)+ ' - ' if self.car_tybe.name else " " + "_") + "   " +"MK: "+ (
                    str(self.Man.setup_id)+ " - " if self.Man.setup_id else " " + "_") + "  " +"MD: "+ (
                                           str(self.model.name)+" - " if self.model.name else " " + "_") + "   " +"YR: "+ (
                                           str(self.year_of_made)+" - " if self.year_of_made else " " + "_") + "  " +"PN: "+ (
                                           str(self.plate_no)+ ' - ' if self.plate_no else " " + "_")+"  "+"CH: "+ (
                                           str(self.chassis_no)+ ' - ' if self.chassis_no else " " + "_")+"  "+"EN: "+ (
                                           str(self.engine)+ ' - ' if self.engine else " " + "_")+"  "+"VCC: "+ (
                                           str(self.motor_cc) if self.motor_cc else " " + "_")
            #
            if  self.type_risk == 'cargo':
                self.risk_description = "FRM: "+(str(self.From)+" - " if self.From else " " + "_") + "   " + "TO: "+(
                    str(self.To)+" - " if self.To else " " + "_") + "   " +"Typ: "+ (
                                           str(self.cargo_type)+" - " if self.cargo_type else " " + "_") + "   " +"WGT: "+ (
                                           str(self.weight) if self.weight else " " + "_")
            if  self.type_risk == 'location':
                self.risk_description = "ADD: "+(str(self.address)+" - " if self.address else " " + "_") + "  " +"TYPE: "+ (
                    str(self.type) if self.type else " " + "_")
        else:
            self.risk_descriptio="aya"

            # if rec.test == "location":
            #     rec.risk_description = (str(rec.group_name) if rec.group_name else " " + "_") + "  " + (
            #         str(rec.count) if rec.count else " " + "_")

    # policy_risk_id = fields.Many2one("policy.broker")

    risks_crm = fields.Many2one("crm.lead", string='Risks')
    # test = fields.Selection(related="policy_risk_id.check_item")
    type_risk = fields.Char(related='risks_crm.test')
    risk_description = fields.Char("Risk Description", compute="_compute_risk_description_crm", store=True)



#
# class dash(models.Model):
#     _name="dash"

