import pandas as pd
import psycopg2
import os
import sys

if __name__ == '__main__':
    if os.path.exists('.env'):
            print('Detected local .env, importing environment from .env...')
            for line in open('.env'):
                var = line.strip().split('=')
                if len(var) == 2:
                    os.environ[var[0]] = var[1]
                    print "Setting environment variable:", var[0]
                    sys.stdout.flush()


def create_answers_df():
    conn = psycopg2.connect(user=os.getenv('USER'), host=os.getenv('HOST'),
                            password=os.getenv('PASSWORD'),
                            dbname=os.getenv('DBNAME'))
    cur = conn.cursor()
    answers_query = ("""SELECT posts.id, body, comment_count, parent_id, score,
                        view_count, bounty_amount
                        FROM posts
                        JOIN votes
                        ON posts.id = votes.post_id
                        WHERE post_type_id=2
                        ORDER BY RANDOM()
                        LIMIT 1000;""")

    a = cur.execute(answers_query)
    answers_df = pd.DataFrame(cur.fetchall(), columns=['id', 'body',
                                'comment_count', 'parent_id', 'score',
                                'view_count', 'bounty_amount'])
    conn.commit()
    conn.close()
    return answers_df
