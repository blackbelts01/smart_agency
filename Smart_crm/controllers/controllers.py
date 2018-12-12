# -*- coding: utf-8 -*-
from odoo import http

# class CrmBlackBelts(http.Controller):
#     @http.route('/crm__black_belts/crm__black_belts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm__black_belts/crm__black_belts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm__black_belts.listing', {
#             'root': '/crm__black_belts/crm__black_belts',
#             'objects': http.request.env['crm__black_belts.crm__black_belts'].search([]),
#         })

#     @http.route('/crm__black_belts/crm__black_belts/objects/<model("crm__black_belts.crm__black_belts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm__black_belts.object', {
#             'object': obj
#         })