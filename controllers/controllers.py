# -*- coding: utf-8 -*-
# from odoo import http


# class Partner-manager/(http.Controller):
#     @http.route('/partner-manager//partner-manager/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner-manager//partner-manager//objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner-manager/.listing', {
#             'root': '/partner-manager//partner-manager/',
#             'objects': http.request.env['partner-manager/.partner-manager/'].search([]),
#         })

#     @http.route('/partner-manager//partner-manager//objects/<model("partner-manager/.partner-manager/"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner-manager/.object', {
#             'object': obj
#         })
