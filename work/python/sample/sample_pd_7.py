import os
from sqlalchemy import create_engine
import pandas as pd
pd.set_option('display.max_columns', 100)

def query_pandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    #埼玉県に市町村はいくつ？(osmで)
    sql = "with saitama_pref as \
    (select * from planet_osm_polygon \
        where name='埼玉県' and admin_level='4') \
    select c.name, c.admin_level from planet_osm_polygon as c, saitama_pref as p \
    where c.admin_level='7' and st_within(c.way, p.way);"

    print(sql)

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
