#!/bin/sh
unzip /work/data/pop_data/data/prefs.zip -d /work/data/pop_data/data

for entry in /work/data/pop_data/data/prefs/*/*/*/*.zip
do
  datapath=`echo $(dirname $entry)`
  unzip -o $entry -d $datapath
  csvname=`echo $datapath'/monthly_mdp_mesh1km.csv'`
  echo $csvname
  echo "COPY pop FROM '$csvname' with (format csv, header true, null '', force_null(population));" >> /work/data/pop_data/copy_csv.sql
done
