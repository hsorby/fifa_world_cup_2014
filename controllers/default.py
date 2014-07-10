# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import operator

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    query = (db.pool_predictions.match_number == db.pool_results.match_number) & (db.auth_user.id == db.pool_predictions.user_id) 
    left = db.pool_predictions.on(db.pool_results.match_result == db.pool_predictions.prediction)
    myrows = db(query).select(left=left, groupby=[db.pool_predictions.user_id, db.pool_predictions.match_number])

    full_table = {}
    user_name_table = {}
    for row in myrows:
        user_id = row.pool_predictions.user_id
#         print row.pool_predictions.user_id, row.auth_user.first_name, row.pool_predictions.prediction
        if user_id not in full_table:
            full_table[user_id] = 0
            user_name_table[user_id] = row.auth_user.first_name
            
        full_table[user_id] += 2
        if row.pool_predictions.prediction == 'Draw':
            full_table[user_id] -= 1

    query = (db.knockout_predictions.match_number == db.knockout_results.match_number) & (db.auth_user.id == db.knockout_predictions.user_id) 
    left = db.knockout_predictions.on(db.knockout_results.match_result == db.knockout_predictions.prediction)
    myrows = db(query).select(left=left, groupby=[db.knockout_predictions.user_id, db.knockout_predictions.match_number])

    for row in myrows:
        user_id = row.knockout_predictions.user_id

        if user_id not in full_table:
            full_table[user_id] = 0
            user_name_table[user_id] = row.auth_user.first_name

        full_table[user_id] += 3
        
        if row.knockout_predictions.match_number == 63:
            full_table[user_id] -= 1
        if row.knockout_predictions.match_number == 64:
            full_table[user_id] += 2

    sorted_full_table = sorted(full_table.iteritems(), key=operator.itemgetter(1))
    sorted_full_table.reverse()
    
    paid = db(db.entrant_status).select()
    eligible = []
    for row in paid:
        if row.paid:
            eligible.append(row.user_id) 
    
    leaderboard = []
    for entry in sorted_full_table:
        user_id = entry[0]
        if user_id in eligible:
            leaderboard.append((user_name_table[user_id], entry[1]))
            
    return dict(leaderboard=leaderboard)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def contactus():
    return dict()

