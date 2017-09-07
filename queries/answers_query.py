import pandas as pd
import psycopg2
import os
import sys


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
