import os
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 100)

def query_geopandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    sql = "with day as \
(select p.name, d.prefcode, d.year, d.month, d.population, p.geom from pop as d inner join pop_mesh as p on p.name = d.mesh1kmid where d.dayflag='0' and d.timezone='0' and d.year='2019' and d.month='01'), \
night as \
(select p.name, d.prefcode, d.year, d.month, d.population, p.geom from pop as d inner join pop_mesh as p on p.name = d.mesh1kmid where d.dayflag='0' and d.timezone='1' and d.year='2019' and d.month='01') \
select poly.name_2, sum(day.population)-sum(night.population) as dif, day.year, day.month, day.prefcode, poly.geom from day, night, adm2 as poly where poly.name_1='Saitama' and st_within(day.geom,poly.geom) and st_within(night.geom,poly.geom) \
group by poly.name_2,day.year, day.month, day.prefcode, poly.geom order by sum(day.population) desc;"

    query_result_gdf = gpd.GeoDataFrame.from_postgis(
        sql, conn, geom_col='geom') #geom_col='way' when using osm_kanto, geom_col='geom' when using gisdb
    return query_result_gdf


def main():

    out = query_geopandas('gisdb') #specify db name
    out['class'] = pd.cut(out['dif'], [-np.inf, -2000000, -1000000, -500000, -100000,-10000,0,10000,100000,500000, np.inf])

    print(out)

    #mapping
    #mapping options: https://geopandas.org/en/stable/docs/user_guide/mapping.html
    fig, ax = plt.subplots(1, 1,figsize=(9,6))
    #out.plot()
    out.plot(column='class', ax=ax, legend=True, cmap='viridis')

    minx=138.5
    maxx=141
    miny=35.5
    maxy= 37
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    plt.savefig('/work/python/sample_mapping2.jpg') #specify filename

if __name__ == '__main__':
    main()
