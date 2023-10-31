import os
from sqlalchemy import create_engine
import pandas as pd
pd.set_option('display.max_columns', 100)

def query_pandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    #さいたま市内のコンビニの総数
    sql = "select count(pt.*) from planet_osm_point pt, adm2 poly \
            where pt.shop='convenience' and \
                poly.name_2='Saitama' and \
                st_within(pt.way,st_transform(poly.geom, 3857));"


    print(sql)

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
