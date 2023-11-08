import os
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 100)

def query_geopandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    sql = "SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom FROM pop AS d INNER JOIN pop_mesh AS p ON p.name = d.mesh1kmid WHERE d.dayflag='0' AND d.timezone='0' AND d.year='2019' and d.month='01';"

    query_result_gdf = gpd.GeoDataFrame.from_postgis(
        sql, conn, geom_col='geom') #geom_col='way' when using osm_kanto, geom_col='geom' when using gisdb
    return query_result_gdf


def main():

    out = query_geopandas('gisdb') #specify db name
    print(out)

    #mapping
    #mapping options: https://geopandas.org/en/stable/docs/user_guide/mapping.html
    fig, ax = plt.subplots(1, 1)
    out.plot(ax=ax)

    #updating map
    #out.plot(column='population', ax=ax, legend=True, cmap='OrRd', scheme='quantiles')
    #spatial extent setting
    #minx=138.5
    #maxx=141
    #miny=35
    #maxy= 37.5
    #ax.set_xlim(minx, maxx)
    #ax.set_ylim(miny, maxy)

    plt.savefig('/work/python/sample_mapping.jpg') #specify filename

if __name__ == '__main__':
    main()
