import pyodbc
import psycopg2
import os
import sys

m_credentials = "DSN={};UID={};PWD={};DATABASE={}".format(os.getenv('DSN'),
                                                          os.getenv('UID'),
                                                          os.getenv('PWD'),
                                                          os.getenv('DATABASE'))
p_credentials = [os.getenv('USER'), os.getenv('HOST'),
                 os.getenv('PASSWORD'), os.getenv('DBNAME')]


def from_mssql_to_psql(m_table, p_table, m_credentials, p_credentials,
                       p_columns, num_columns):
    """
    Connects to a remote Microsoft SQL Server table and moves it to an
    already-made, remote table in Postgres.

    PARAMETERS:
        m_table: str, name of table in SQL Server to be moved to Postgres
        p_table: str, name of destination table in Postgres
        m_credentials: str, credentials for SQL Server, in order DSN, UID,
                       PWD, DATABASE
        p_credentials: list of str, credentials for Postgres, in order user,
                       host, password, dbname
        p_columns = tuple of str, names of the columns in the Postgres table
        num_columns = number of columns being transferred

    RETURNS:
        Nothing. Check your Postgres database to see results.
    """

    mconn = pyodbc.connect({}).format(m_credentials)
    mcursor = mconn.cursor()
    m_query = "SELECT * FROM {};".format(m_table)

    pconn = psycopg2.connect(user=p_credentials[0], host=p_credentials[1],
                             password=p_credentials[2],
                             dbname=p_credentials[3])
    pcursor = pconn.cursor()

    for row in mcursor.execute(m_query).fetchall():
        cols_str = "INSERT INTO {} {}".format(p_table, p_columns)
        val_str = "VALUES ({}%s);".format('%s, ' * (num_columns-1))
        insert = pcursor.execute(cols_str + val_str, row)
        pconn.commit()

    mcursor.close()
    msconn.close()

    pcursor.close()
    pconn.close()


if __name__ == '__main__':
    if os.path.exists('.env'):
            print('Detected local .env, importing environment from .env...')
            for line in open('.env'):
                var = line.strip().split('=')
                if len(var) == 2:
                    os.environ[var[0]] = var[1]
                    print "Setting environment variable:", var[0]
                    sys.stdout.flush()
