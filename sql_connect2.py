import pyodbc
import psycopg2
import pandas as pd

msconn = pyodbc.connect('DSN=sosql2;UID=SA;PWD=Corinn3!;DATABASE=ms_stack_overflow')
mcur = msconn.cursor()
#query = ("SELECT COLUMN_NAME, DATA_TYPE FROM user_tab_columns WHERE table_name='Comments';")
#query = ("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=Posts;")
query = ("SELECT TOP 2 * FROM Comments;")
row = mcur.execute(query).fetchall()
print(row)
#df = pd.read_sql(sql, msconn)
#print(df.head())

# crsr.close()
# conn.close()

pconn = psycopg2.connect(user='postgres', host='54.183.199.217', password='postgres', dbname='tester')
pcur = pconn.cursor()
format('Hello %s, %1$s', 'World')
insertion = format("INSERT INTO comments ")

# SELECT DATA_TYPE
# FROM INFORMATION_SCHEMA.COLUMNS
# WHERE
#      TABLE_NAME = 'yourTableName' AND
#      COLUMN_NAME = 'yourColumnName'

# sqlcmd -S localhost -U SA -P Corinn3!

# from ~/.ssh
# ssh -i capstone.pem ubuntu@54.67.1.205

# [sosql]
# Description = Stack Overflow for capstone
# Driver=/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.7.0
# Trace = No
# Server = ec2-54-67-1-205.us-west-1.compute.amazonaws.com
