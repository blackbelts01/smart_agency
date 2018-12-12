# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import SUPERUSER_ID
import re
from odoo.exceptions import ValidationError
class Users(models.Model):
    _inherit = 'res.users'


    country= fields.Many2one('res.country',string='Country')
    agency=fields.Many2one('agency', string='Agency Number' ,domain="[('country','=',country)]")
    userid= fields.Integer(string='User Id')
    firstname=fields.Char('First Name',required=True)
    lastname = fields.Char('Last Name', required=True)
    name=fields.Char(string='User Name',readonly=True)
    space= fields.Char(' ', readonly=True)


    @api.onchange('agency')
    def onchange_user_id(self):
        record_ids = self.search([('agency', '=', self.agency.id)], order='id desc', limit=1)
        last_id = record_ids.userid
        self.userid =last_id + 1

    @api.onchange('userid')
    def change_name(self):
        self.name=str(self.country.name[0:3])+'_'+str(self.agency.agency_no)+'_'+str(self.firstname[0:2])+'_'+str(self.lastname[0:2])+'_'+str(self.userid)


    @api.onchange('login')
    def validate_mail(self):
        if self.login:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.login)
            if match == None:
                raise ValidationError('Invalid Mail')


    @api.model
    def create(self, vals):
        country = vals.get('country')
        if country:
            ct_name = self.env['res.country'].browse(country).name[0:3]
            agency_id = vals.get('agency')
            if agency_id:
                agency_no=self.env['agency'].browse(agency_id).agency_no
                last_user = self.search([('agency', '=', agency_id)], order='id desc', limit=1)
                vals['userid']=last_user.userid+1
                firstn=vals.get('firstname')
                lname=vals.get('lastname')
                userid=vals.get('userid')
                vals['name']=ct_name+'_'+str(agency_no)+'_'+firstn+'_'+lname+'_'+str(last_user.userid+1)
        return super(Users, self).create(vals)

    @api.multi
    def write(self, vals):
                firstn = vals.get('firstname')
                lname = vals.get('lastname')
                userid = vals.get('userid')
                country = vals.get('country')
                agency_id = vals.get('agency')
                fname=''
                ln=''
                uid=''
                if agency_id:
                    last_user = self.search([('agency', '=', agency_id)], order='id desc', limit=1)
                    vals['userid']=last_user.userid+1
                    userid = last_user.userid+1



                if country:
                    ct_name = self.env['res.country'].browse(country).name[0:3]
                else:
                    country = self.country.id
                    ct_name=self.env['res.country'].browse(country).name[0:3]

                if agency_id:
                    agency_no = self.env['agency'].browse(agency_id).agency_no
                else:
                    agency_id=self.agency.id
                    agency_no = self.env['agency'].browse(agency_id).agency_no


                if firstn:
                     fname=firstn
                else:
                    fname=self.firstname
                if lname:
                    ln=lname
                else:
                    ln=self.lastname
                if userid:
                     uid=userid
                else:
                    uid=self.userid

                vals['name'] = ct_name+'_'+str(agency_no)+'_'+fname+'_'+ln+"_"+str(uid)

                return super(Users, self).write(vals)

    @api.multi
    def name_get(self):
        res = []
        ids = self.env['res.users'].search([('name', '=', 'Ang_4_ali_khaled_1')], limit=1).id
        if self._context.get('filter_own_user', False) and self._uid != ids:
            users = self.browse([self._uid, ids])
        else:
            users = self
        return super(Users, users).name_get()






class Agencies(models.Model):
    _name ='agency'
    _rec_name='agency_no'
    agency_no=fields.Integer('Agency_No')
    country=fields.Many2one('res.country',string='country')



# class partner(models.Model):
#     _inherit='res.partner'
#     name=fields.Char(readonly=True,required=False)
#     DOB=fields.Date('Date of Birth')
#     martiual_status = fields.Selection([('Single', 'Single'),
#                                         ('Married', 'Married'),],
#                                        'marital status', track_visibility='onchange')
#     last_time_insure = fields.Date('last_time_insure')
#
#     C_industry = fields.Selection([('Software', 'Software'),
#                                    ('Engineering', 'Engineering'), ],
#                                   'Industry', track_visibility='onchange')
#     holding=fields.Many2one('res.partner',string='Holding Company')
#
#
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        ids = self.env['res.users'].search([('name', '=', 'Ang_4_ali_khaled_1')], limit=1).id
        if self._context.get('own_customer_only'):
            if self.env.user.id != 1 and self.env.user.id != ids :
                args+=[('user_id','=',self.env.user.id)]
        print (args)
        return super(partner, self).search(args, offset=offset, limit=limit, order=order, count=count)