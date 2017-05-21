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


def create_questions_df(row_limit):
    conn = psycopg2.connect(user=os.getenv('USER'), host=os.getenv('HOST'),
                            password=os.getenv('PASSWORD'),
                            dbname=os.getenv('DBNAME'))
    cur = conn.cursor()
    percent = row_limit/5e7*100
    fast_sample = ("""SELECT id, accepted_answer_id, answer_count, body,
                      comment_count, favorite_count, score, tags, title,
                      view_count, creation_date
                      FROM posts TABLESAMPLE SYSTEM ({})
                      WHERE post_type_id=1;""").format(percent)
    # questions_query = ("""SELECT posts.id, accepted_answer_id, answer_count, body,
    #                     comment_count, favorite_count, score, tags, title,
    #                     view_count, bounty_amount, posts.creation_date
    #                     FROM posts
    #                     JOIN votes
    #                     ON posts.id = votes.post_id
    #                     WHERE post_type_id=1
    #                     ORDER BY RANDOM()
    #                     LIMIT {};""").format(row_limit)

    try:
        q = cur.execute(questions_query)
    except Exception as e:
        print e.message
        conn.rollback()  # Rollback to prevent session locking out

    questions_df = pd.DataFrame(cur.fetchall(), columns=['id', 'accepted_answer_id',
                        'answer_count', 'body', 'comment_count', 'favorite_count',
                        'score', 'tags', 'title', 'view_count', 'creation_date'])
    conn.commit()
    cur.close()
    conn.close()
    return questions_df
