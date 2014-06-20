'''
Created on Jun 12, 2014

@author: hsorby
'''

def _initialisePredictions():
    all_matches = db(db.pool_match.match_number>0).select(db.pool_match.match_number)
    all_predictions = db(db.pool_predictions.user_id==auth.user_id).select(db.pool_predictions.match_number, groupby=db.pool_predictions.match_number)
    if len(all_predictions) != len(all_matches):
        all_match_numbers = [row.match_number for row in all_matches]
        all_user_match_numbers = [row.match_number for row in all_predictions]
        for match_number in all_match_numbers:
            if match_number not in all_user_match_numbers:
                db.pool_predictions.insert(match_number=match_number,
                                           user_id=auth.user_id,
                                           prediction=None)

@auth.requires_login()
def index():
    import datetime
    db.pool_match.id.readable=False
    db.pool_match.expires.readable=False
    query = (db.pool_match.expires >= datetime.datetime.now()) & (db.pool_predictions.user_id == auth.user_id)
    test_query = (db.pool_match.expires >= datetime.datetime.now())
    fields = [db.pool_match.match_number, db.pool_match.home_team, db.pool_match.away_team, db.pool_match.uuid, db.pool_predictions.prediction]
    left = db.pool_predictions.on((db.pool_match.match_number == db.pool_predictions.match_number))
    
    _initialisePredictions()
    
    grid = SQLFORM.grid(query, fields=fields, left=left, groupby=db.pool_predictions.match_number,create=False,editable=auth.has_membership('manage'),deletable=False,details=False,
                        csv=auth.has_membership('manage'), paginate=25,
                        links=[lambda row: A('predict   ',_href=URL('predict_match',args=row.pool_match.uuid),_class="btn")])
    
    return locals()

@auth.requires_membership('manage')
def create_match():
    def f(form):
        form.vars.results = [0]*3
    from gluon.utils import web2py_uuid
    db.pool_match.uuid.default = uuid = web2py_uuid()
    form = SQLFORM(db.pool_match).process( onvalidation=f)
    if form.accepted:
        redirect(URL('index',args=uuid))
    return locals()

def predict_match():
    uuid = request.args(0)
    pool_match = db.pool_match(uuid=uuid) or redirect(URL('index'))
    if request.post_vars:
        returned_choice = request.post_vars.choice
        db.pool_predictions.update_or_insert((db.pool_predictions.match_number==pool_match.match_number) &( db.pool_predictions.user_id==auth.user_id),
                                   match_number=pool_match.match_number,
                                   user_id=auth.user_id,
                                   prediction=returned_choice)
        redirect(URL('index'))
        
    return locals()
