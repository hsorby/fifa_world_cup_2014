'''
Created on Jun 14, 2014

@author: hsorby
'''
db.define_table('entrant_status',
                Field('user_id','reference auth_user'),
                Field('paid','boolean'))
