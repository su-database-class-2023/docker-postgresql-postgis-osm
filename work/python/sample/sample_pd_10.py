import os
from sqlalchemy import create_engine
import pandas as pd
pd.set_option('display.max_columns', 100)

def query_pandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    #埼玉市内の駅周辺（半径300 m）のコンビニはいくつ？
    sql = "select buffer.name, count(DISTINCT(pt.osm_id)) from planet_osm_point as pt, \
            (select pt.osm_id, pt.name, st_buffer (pt.way, 300) \
                from planet_osm_point pt, adm2 poly2 \
            where pt.railway='station' and poly2.name_2='Saitama' and \
            st_within(pt.way,st_transform(poly2.geom, 3857))) as buffer, adm2 as poly \
            where pt.shop='convenience' and poly.name_2='Saitama' and \
            ST_Within(pt.way,buffer.st_buffer) \
            group by buffer.name order by count desc;"


    print(sql)

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
