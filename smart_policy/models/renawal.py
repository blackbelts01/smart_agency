from odoo import api, fields, models

class insurancePolicy(models.Model):
    _inherit = 'policy.broker'

    @api.multi
    def create_renewal(self):
        view = self.env.ref('smart_policy.policy_form_view')

        risk = self.env["policy.risk"].search([('id', 'in', self.new_risk_ids.ids)])
        records_risk = []
        for rec in risk:
            object = (0, 0,{'risk_description': rec.risk_description,'old_id': rec.id,
                       'car_tybe':rec.car_tybe.id, 'motor_cc':rec.motor_cc, 'year_of_made':rec.year_of_made, 'model':rec.model.id, 'Man':rec.Man.id,
                       'name':rec.name, 'DOB':rec.DOB, 'job':rec.job.id,
                       'From':rec.From, 'To':rec.To, 'cargo_type':rec.cargo_type, 'weight':rec.weight,
                       'address':rec.address , 'type':rec.type,
                       'group_name': rec.group_name, 'count': rec.count, 'file': rec.file,

                       })
            records_risk.append(object)

        coverlines = self.env["covers.lines"].search([('id', 'in', self.name_cover_rel_ids.ids)])
        records_cover = []
        for rec in coverlines:
            covers = (0, 0,
                      {
                       'old_risk_id':rec.riskk.id,
                       'name1': rec.name1.id,
                       'check': rec.check,
                       'sum_insure': rec.sum_insure,
                       'deductible': rec.deductible,
                       'limitone': rec.limitone,
                       'limittotal': rec.limittotal,
                       'rate': rec.rate,
                       'net_perimum': rec.net_perimum,
                       }
                      )
            records_cover.append(covers)

        share_commission = self.env["insurance.share.commission"].search([('id', 'in', self.share_commission.ids)])
        records_commission = []
        for rec in share_commission:
            comm = (0, 0,
                    {'agent': rec.agent.id,
                     'commission_per': rec.commission_per,
                       })
            records_commission.append(comm)

        installments = self.env["installment.installment"].search([('id', 'in', self.rella_installment_id.ids)])
        records_installments = []
        for rec in installments:
            install = (0, 0,
                       {'date': rec.date,
                        'amount': rec.amount,
                        'state': rec.state,
                       })
            records_installments.append(install)



        return {
            'name': ('Policy'),
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'res_model': 'policy.broker',
            'target': 'current',
            'type': 'ir.actions.act_window',
            # 'flags': {'form': {'options': {'mode': 'view'}}},
            'context': {
                'default_renwal_check': True,
                'default_policy_number': self.std_id,
                'default_company': self.company.id,
                'default_ins_type': self.ins_type,
                'default_line_of_bussines': self.line_of_bussines.id,
                'default_product_policy': self.product_policy.id,
                'default_insurance_type': self.insurance_type,
                'default_customer': self.customer.id,
                'default_issue_date': self.issue_date,
                'default_start_date': self.start_date,
                'default_end_date': self.end_date,
                'default_branch': self.branch.id,
                'default_salesperson': self.salesperson.id,
                'default_currency_id': self.currency_id.id,
                'default_benefit': self.benefit,
                'default_term': self.term,
                'default_no_years': self.no_years,
                'default_gross_perimum': self.gross_perimum,
                'default_commision': self.commision,
                'default_com_commision': self.com_commision,
                'default_earl_commision': self.earl_commision,
                'default_fixed_commision': self.fixed_commision,
                'default_total_commision': self.total_commision,

                'default_new_risk_ids': records_risk,
                'default_share_commission': records_commission,
                'default_rella_installment_id': records_installments,
                'default_name_cover_rel_ids': records_cover,
            }
        }
