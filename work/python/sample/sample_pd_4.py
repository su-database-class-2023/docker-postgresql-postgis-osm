import os
from sqlalchemy import create_engine
import pandas as pd
pd.set_option('display.max_columns', 100)

def query_pandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    #埼玉県で一番小さい面積の市町村を調べる
    sql = "select name_2, st_area(geom::geography)/1000000 as area_km2 \
          from adm2 \
          where name_1='Saitama' AND \
          st_area(geom::geography)/1000000 = \
          (select min(st_area(geom::geography)/1000000) from adm2 where name_1='Saitama'); "
    print(sql)

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
