'''
Created on Jun 14, 2014

@author: hsorby
'''
db.define_table('knockout_match',
                Field('match_number','integer',requires=IS_NOT_EMPTY()),
                Field('home_team','string',requires=IS_NOT_EMPTY()),
                Field('away_team','string',requires=IS_NOT_EMPTY()),
                Field('expires', 'datetime', requires=IS_DATETIME()),
                Field('uuid',readable=False,writable=False))

# db.knockout_match.truncate()
# db.commit()
# print db._lastsql

db.define_table('knockout_predictions',
                Field('match_id', 'integer'),
                Field('user_id', 'reference auth_user'),
                Field('prediction', 'string'))

# db.knockout_predictions.truncate()
# db.commit()

db.define_table('knockout_results',
                Field('match_id','integer'),
                Field('match_result','string'))

# db.knockout_results.truncate()
# db.commit()

db.define_table('knockout_home_team_map',
                Field('teamkey', 'string'),
                Field('teamname', 'string'))

# db.knockout_home_team_map.truncate()
# db.commit()

db.define_table('knockout_away_team_map',
                Field('teamkey', 'string'),
                Field('teamname', 'string'))

# db.knockout_home_team_map.truncate()
# db.commit()

db.define_table('knockout_pred_team_map',
                Field('teamkey', 'string'),
                Field('teamname', 'string'))

# db.knockout_pred_team_map.truncate()
# db.commit()
