from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError

class insurancePolicyinhrit(models.Model):
    _inherit = 'policy.broker'


    @api.multi
    def show_claim(self):
        return {
            'name': ('Claim'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'insurance.claim',  # model name ?yes true ok
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {'default_policy_number': self.id},
            'domain': [('policy_number', '=', self.id)]
        }



    count_claim = fields.Integer(compute="_compute_claim",copy=True)

    @api.one
    def _compute_claim(self):
        self.count_claim = 0
        self.count_claim = self.env['insurance.claim'].search_count([('policy_number', '=', self.id)])