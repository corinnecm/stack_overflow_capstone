import pandas as pd
import psycopg2
import os
import sys


def create_questions_df(row_limit):
    conn = psycopg2.connect(user=os.getenv('USER'), host=os.getenv('HOST'),
                            password=os.getenv('PASSWORD'),
                            dbname=os.getenv('DBNAME'))
    cur = conn.cursor()
    percent = (row_limit/5e7)*100
    fast_sample = ("""SELECT id, accepted_answer_id, answer_count, body,
                      comment_count, favorite_count, score, tags, title,
                      view_count, creation_date
                      FROM posts TABLESAMPLE SYSTEM ({})
                      WHERE post_type_id=1;""").format(percent)

    try:
        q = cur.execute(fast_sample)
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
