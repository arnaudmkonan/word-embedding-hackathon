import psycopg2 as pg
import pandas as pd
import datetime, time
import pickle

# DB and Query vars
pg_conn_str =  os.getenv("ARTHUR_REFACTOR_DB_CONN_STRING", "postgres://localhost:5432/arthurrefactor")
# sql_file_name = "./arthur_construction_binary.sql"
sql_file_name = "./arthur_office_jockey.sql"

def run_sql_file(filename, connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    '''
    start = time.time()
    
    file = open(filename, 'r')
    sql = " ".join(file.readlines())
    print("Start executing: " + filename + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql) 
  
    df = pd.read_sql_query(sql, con=connection)
    end = time.time()
    print( "Time elapsed to run the query:")
    print(str((end - start)*1000) + ' ms')
    return df

conn = pg.connect(pg_conn_str)
arthur_binary_df = run_sql_file(sql_file_name, conn)
pickle.dump( arthur_binary_df, open( "data_office_jockey.pickle", "wb" ) )
