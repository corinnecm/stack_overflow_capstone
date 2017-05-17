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


def create_questions_df():
    conn = psycopg2.connect(user=os.getenv('USER'), host=os.getenv('HOST'),
                            password=os.getenv('PASSWORD'),
                            dbname=os.getenv('DBNAME'))
    cur = conn.cursor()
    questions_query = ("""SELECT posts.id, accepted_answer_id, answer_count, body,
                        comment_count, favorite_count, score, tags, title,
                        view_count, bounty_amount
                        FROM posts
                        JOIN votes
                        ON posts.id = votes.post_id
                        WHERE post_type_id=1
                        ORDER BY RANDOM()
                        LIMIT 1000;""")

    q = cur.execute(questions_query)
    questions_df = pd.DataFrame(cur.fetchall(), columns=['id', 'accepted_answer_id',
                        'answer_count', 'body', 'comment_count', 'favorite_count',
                        'score', 'tags', 'title', 'view_count', 'bounty_amount'])
    conn.commit()
    conn.close()
    return questions_df
