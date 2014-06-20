'''
Created on Jun 13, 2014

@author: hsorby
'''
db.define_table('pool_match',
                Field('match_number','integer',requires=IS_NOT_EMPTY()),
                Field('home_team','string',requires=IS_NOT_EMPTY()),
                Field('away_team','string',requires=IS_NOT_EMPTY()),
                Field('expires', 'datetime', requires=IS_DATETIME()),
                Field('uuid',readable=False,writable=False))

# db.pool_match.truncate()
# db.commit()

db.define_table('pool_predictions',
                Field('match_number','reference pool_match'),
                Field('user_id', 'reference auth_user'),
                Field('prediction','string'))

# db.pool_predictions.truncate()
# db.commit()

db.define_table('pool_results',
                Field('match_number','reference pool_match'),
                Field('match_result','string'))

# db.pool_results.truncate()
# db.commit()
