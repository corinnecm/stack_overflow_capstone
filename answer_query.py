import pandas as pd
import psycopg2
import os
import sys

# if __name__ == '__main__':
#     if os.path.exists('.env'):
#             print('Detected local .env, importing environment from .env...')
#             for line in open('.env'):
#                 var = line.strip().split('=')
#                 if len(var) == 2:
#                     os.environ[var[0]] = var[1]
#                     print "Setting environment variable:", var[0]
#                     sys.stdout.flush()


def create_answers_df(row_limit):
    conn = psycopg2.connect(user=os.getenv('USER'), host=os.getenv('HOST'),
                            password=os.getenv('PASSWORD'),
                            dbname=os.getenv('DBNAME'))
    cur = conn.cursor()
    percent = row_limit/5e7*100
    fast_sample = ("""SELECT id, body, comment_count, parent_id, score,
                      view_count, creation_date
                      FROM posts TABLESAMPLE SYSTEM ({})
                      WHERE post_type_id=2;""").format(percent)
    # answers_query = ("""SELECT posts.id, body, comment_count, parent_id, score,
    #                     view_count, bounty_amount, posts.creation_date
    #                     FROM posts
    #                     JOIN votes
    #                     ON posts.id = votes.post_id
    #                     WHERE post_type_id=2
    #                     ORDER BY RANDOM()
    #                     LIMIT {};""").format(row_limit)

    try:
        a = cur.execute(fast_sample)
    except Exception as e:
        print e.message
        conn.rollback()  # Rollback to prevent session locking out

    answers_df = pd.DataFrame(cur.fetchall(), columns=['id', 'body',
                                'comment_count', 'parent_id', 'score',
                                'view_count', 'creation_date'])
    conn.commit()
    cur.close()
    conn.close()
    return answers_df
