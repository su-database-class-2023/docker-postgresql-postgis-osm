import os
from sqlalchemy import create_engine
import pandas as pd
pd.set_option('display.max_columns', 100)

def query_pandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    # adm2データをチェックする
    sql = "select * from adm2 limit 3;"
    print(sql)

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
