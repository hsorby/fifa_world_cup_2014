'''
Created on Jun 12, 2014

@author: hsorby
'''
def _initialisePredictions():
    all_matches = db(db.knockout_match.match_number>0).select(db.knockout_match.match_number)
    all_predictions = db(db.knockout_predictions.user_id==auth.user_id).select(db.knockout_predictions.match_id, groupby=db.knockout_predictions.match_id)

    if len(all_predictions) != len(all_matches):
        all_match_numbers = [row.match_number for row in all_matches]
        all_user_match_numbers = [row.match_number for row in all_predictions]
        for match_number in all_match_numbers:
            if match_number not in all_user_match_numbers:
                db.knockout_predictions.insert(match_id=match_number,
                                           user_id=auth.user_id,
                                           prediction=None)

@auth.requires_login()
def index():
    import datetime
    db.knockout_match.id.readable=False
    db.knockout_match.expires.readable=False
    original_query = (db.knockout_match.expires >= datetime.datetime.now()) & (db.knockout_predictions.user_id == auth.user_id)
    test_query = (db.knockout_match.expires >= datetime.datetime.now()) #& ((db.knockout_home_team_map.teamkey == db.knockout_match.home_team) & (db.knockout_away_team_map.teamkey == db.knockout_match.away_team))
    fields = [db.knockout_match.match_number, db.knockout_home_team_map.teamname, db.knockout_away_team_map.teamname, db.knockout_match.uuid, db.knockout_pred_team_map.teamname]
    headers = {'knockout_match.match_number': 'Match Number',
           'knockout_home_team_map.teamname': 'Home Team',
           'knockout_away_team_map.teamname': 'Away Team',
           'knockout_pred_team_map.teamname': 'Prediction' }
    left = [db.knockout_predictions.on(db.knockout_match.match_number == db.knockout_predictions.match_id), 
            db.knockout_home_team_map.on(db.knockout_home_team_map.teamkey == db.knockout_match.home_team),
            db.knockout_pred_team_map.on(db.knockout_pred_team_map.teamkey == db.knockout_predictions.prediction),
            db.knockout_away_team_map.on(db.knockout_away_team_map.teamkey == db.knockout_match.away_team)]
    
    _initialisePredictions()
    
    grid = SQLFORM.grid(test_query, fields=fields, left=left, headers=headers, groupby=db.knockout_match.match_number,create=False,editable=auth.has_membership('manage'),deletable=False,details=False,
                        csv=auth.has_membership('manage'), paginate=25,
                        links=[lambda row: A('predict   ',_href=URL('predict_match',args=row.knockout_match.uuid),_class="btn")])
    return locals()

@auth.requires_membership('manage')
def create_match():
    def f(form):
        form.vars.results = [0]*2
    from gluon.utils import web2py_uuid
    db.knockout_match.uuid.default = uuid = web2py_uuid()
    form = SQLFORM(db.knockout_match).process( onvalidation=f)
    if form.accepted:
        redirect(URL('index',args=uuid))
    return locals()

def predict_match():
    uuid = request.args(0)
    knockout_match = db.knockout_match(uuid=uuid) or redirect(URL('index'))
    result_home = db(knockout_match.home_team==db.knockout_home_team_map.teamkey).select(db.knockout_home_team_map.teamname)
    for row in result_home:
        home_team = row['teamname']
    result_away = db(knockout_match.away_team==db.knockout_away_team_map.teamkey).select(db.knockout_away_team_map.teamname)
    for row in result_away:
        away_team = row['teamname']
    if request.post_vars:
        returned_choice = request.post_vars.choice
        db.knockout_predictions.update_or_insert((db.knockout_predictions.match_id==knockout_match.match_number) &( db.knockout_predictions.user_id==auth.user_id),
                                    match_id=knockout_match.match_number,
                                    user_id=auth.user_id,
                                    prediction=returned_choice)
        redirect(URL('index'))
    return locals()
