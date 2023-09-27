import os
from sqlalchemy import create_engine
import pandas as pd
pd.set_option('display.max_columns', 100)

def query_pandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    #埼玉市内の駅周辺（半径300 m）のコンビニはいくつ？
    sql = "WITH buffer AS \
            (SELECT pt.osm_id, pt.name, ST_Buffer(pt.way, 300) \
                FROM planet_osm_point pt, adm2 poly2 \
                WHERE pt.railway='station' AND \
                    poly2.name_2='Saitama' AND \
                    ST_Within(pt.way,st_transform(poly2.geom, 3857)))\
          SELECT buffer.name, count(DISTINCT(pt.osm_id)) \
            FROM planet_osm_point AS pt, buffer, adm2 AS poly2 \
            WHERE pt.shop='convenience' AND \
                  poly2.name_2='Saitama' AND \
                  ST_Within(pt.way,buffer.st_buffer) \
            GROUP BY buffer.name \
            ORDER BY count desc;"


    print(sql)

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
