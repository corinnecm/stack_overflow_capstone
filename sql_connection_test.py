import pypyodbc

conn = pypyodbc.connect(driver='{Microsoft ODBC Driver 13 for SQL Server}',
                        server='ec2-54-67-1-205.us-west-1.compute.amazonaws.com',
                        port='1433',
                        database='stack_overflow',
                        uid='SA',
                        pwd='Corinn3!')

cursor = conn.cursor()

query = "SELECT * FROM votes LIMIT 5;"

cursor.execute("")

# Driver = {SQL Server Native Client 11.0}}
