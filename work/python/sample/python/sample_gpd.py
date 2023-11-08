import os
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
pd.set_option('display.max_columns', 100)

def query_geopandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    sql = "select * from adm2 limit 3;"

    query_result_gdf = gpd.GeoDataFrame.from_postgis(
        sql, conn, geom_col='geom') #geom_col='way' when using osm_kanto, geom_col='geom' when using gisdb
    return query_result_gdf


def main():

    out = query_geopandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
