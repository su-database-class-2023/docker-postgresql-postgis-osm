import os
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 100)

def query_geopandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    # 埼玉県内市町村ごとの2019年1月の休日昼間人口集計
    sql = "with pop as \
                (select p.name, d.prefcode, d.year, d.month, d.population, p.geom \
                    from pop as d \
                        inner join pop_mesh as p \
                            on p.name = d.mesh1kmid \
                        where d.dayflag='0' and \
                              d.timezone='0' and \
                              d.year='2019' and \
                              d.month='01') \
            select poly.name_2, sum(pop.population) as sum, pop.year, pop.month, pop.prefcode, poly.geom \
                from pop, adm2 as poly \
                where poly.name_1='Saitama' and \
                      st_within(pop.geom,poly.geom) \
                group by poly.name_2,pop.year, pop.month, pop.prefcode, poly.geom \
                order by sum(pop.population) desc;"

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
    out.plot(column='sum', ax=ax, legend=True, cmap='viridis')
    #spatial extent setting
    #minx=138.5
    #maxx=141
    #miny=35
    #maxy= 37.2
    #ax.set_xlim(minx, maxx)
    #ax.set_ylim(miny, maxy)

    plt.savefig('/work/python/sample_mapping_11.jpg') #specify filename

if __name__ == '__main__':
    main()
