# 1. create db
At terminal
```
createdb -U postgres gisdb
```
# 2. connect to db
At terminal
```
psql -U postgres gisdb
```
# 3. activate postgis extension
```
create extension postgis;
```
# 4. disconnect db
```
\q
```
# 5. obtain osm data
At terminal
```
wget -P /work/data/osm --no-check-certificate https://download.geofabrik.de/asia/japan/kanto-latest.osm.pbf
```
# 5. change permission
At terminal
```
cd /work/data/osm
chmod +x /work/data/osm/default.style
chmod +x /work/data/osm/kanto-latest.osm.pbf
```

# 6. create table schema
At working directory (`/work/data/osm`)where [osm data](http://download.geofabrik.de/asia/japan.html) and [default.style](https://learnosm.org/files/default.style) are located:
```
osm2pgsql --create --database=gisdb --slim --style=./default.style -U postgres -H localhost ./kanto-latest.osm.pbf
```
# 7. wait & wait & wait

# reference:
- https://qiita.com/hiyuzawa/items/ba1b9de36bf911145c1c