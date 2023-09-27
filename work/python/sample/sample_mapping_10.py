import os
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 100)

def query_geopandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    # 2019年1月と2020年4月の休日昼間人口の差
    sql = "WITH pop2019 AS \
                    (SELECT * \
                        FROM pop INNER JOIN pop_mesh \
                            ON pop_mesh.name = pop.mesh1kmid \
                                WHERE dayflag='0' AND \
                                    timezone='0' AND \
                                    year='2019' AND \
                                    month='01'), \
                pop2020 AS \
                    (SELECT mesh1kmid, population \
                        FROM pop INNER JOIN pop_mesh \
                            ON pop_mesh.name = pop.mesh1kmid \
                                WHERE dayflag='0' AND \
                                    timezone='0' AND \
                                    year='2020' AND \
                                    month='04') \
            SELECT pop2019.mesh1kmid,  pop2019.population as pop19, pop2020.population as pop20, (pop2019.population - pop2020.population) AS dif19_20, pop2019.geom \
                    FROM pop2019 \
                    INNER JOIN pop2020 \
                        ON pop2019.mesh1kmid = pop2020.mesh1kmid \
                    GROUP BY pop2019.mesh1kmid, pop2019.population, pop2020.population, pop2019.geom \
                    ORDER BY pop2019.mesh1kmid;"

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
    out.plot(column='dif19_20', ax=ax, legend=True, cmap='viridis')
    #spatial extent setting
    minx=138.5
    maxx=141
    miny=35
    maxy= 37.2

    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    plt.savefig('/work/python/sample_mapping_10.jpg') #specify filename

if __name__ == '__main__':
    main()
