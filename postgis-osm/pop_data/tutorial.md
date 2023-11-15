# Import spatial data to postgreSQL

データベースシステム講義資料
version 0.0.1
authors: N. Tsutsumida

Copyright (c) 2023 Narumasa Tsutsumida
Released under the MIT license
https://opensource.org/licenses/mit-license.php


## 1. 境界データのインポート
はじめに、日本の市町村の境界を示す`JPN_adm2.shp`をインポートしてみよう。

### 1.1 データベースの作成
`gisdb`というデータベースを作成する。
```sh
createdb -U postgres gisdb
```
### 1.2. postgis extensionの有効化
```sql
psql -U postgres gisdb -c "create extension postgis"
```

### 1.3. sqlコマンドの作成
`shp2pgsql`でshpファイルをpostGISにインポートするためのsqlコマンドを作成する。

```sh
shp2pgsql -D -I -s 4326 /work/data/pop_data/JPN_adm/JPN_adm2.shp adm2 > /work/data/pop_data/JPN_adm/adm2.sql
```
-D: ダンプ形式にする
-I: 空間インデックスを作成
-s: 座標系を定義（4326はespgコードで、WGS84）
`JPN_adm2.shp`はがインポートするshpファイル
`adm2`は追加するテーブル名
`/work/data/pop_data/JPN_adm/adm2.sql`は変換するsqlコマンドが記載されたファイル

### 1.4. DBへの追加
1.3で作成したsqlコマンドを用いてgisdb DBへデータを追加する。

```sh
psql -U postgres -d gisdb -f /work/data/pop_data/JPN_adm/adm2.sql
```

### 1.5 pythonで描写
TBD

## 2. openstreetmapデータベースの構築
openstreetmapで取得し、データを入力してみよう。
かなりの時間がかかる（私の環境では3時間程）ので余裕をもって実施すること。
### 2.1. OSMデータの取得
[osm data](http://download.geofabrik.de/asia/japan.html)から関東地域のデータ(.osm.pbf)をダウンロードする。
```
wget -P /work/data/osm --no-check-certificate https://download.geofabrik.de/asia/japan/kanto-latest.osm.pbf
```

### 2.2 ファイルの権限変更
```
cd /work/data/osm
chmod +x /work/data/osm/default.style
chmod +x /work/data/osm/kanto-latest.osm.pbf
```

### 2.3. スキーマの作成とデータ入力
[osm data](http://download.geofabrik.de/asia/japan.html)と[default.style](https://learnosm.org/files/default.style)のあるディレクトリ `/work/data/osm` をカレントディレクトリとし、以下を実行する。

```sh
osm2pgsql --create --database=gisdb --slim --style=./default.style -U postgres -H localhost ./kanto-latest.osm.pbf
```
（注意）かなり時間がかかります。


## 3. 人流データのインポート

データは(G空間情報センター)[https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto]より取得している。
1km^2でかつ一月ごとの集計データが入手可能。
データのダウンロードに時間がかかるので、すでに入手したものを`/work/data/pop_data/data`に`mesh1.zip`と`prefs.zip`をおいている。
`mesh1.zip`には、1km^2のグリッドデータ`mesh1.shp`がふくまれており、人流データの各データの位置と範囲を規定している。
`prefs.zip`には関東圏の1都6県の月別の人流データが格納されている。
この講義では負荷軽減のため感染拡大前の2019年1月、東京・神奈川・埼玉・千葉で緊急事態宣言が発出された期間（2020/4/7-2020/5/21）におおよそあたる2020年4月の集計データのみを使用する。

### 3.1. meshデータ
`mesh1.zip`を解凍する。

```
unzip /work/data/pop_data/data/mesh1.zip -d /work/data/pop_data/data
```

#### 3.1.1. sqlコマンドの作成
shp2pgsqlでshpファイルをpostGISにインポートするためのsqlコマンドを作成する。

```sh
shp2pgsql -D -I -s 4326 /work/data/pop_data/data/mesh1/mesh1.shp pop_mesh > /work/data/pop_data/data/mesh1/mesh1.sql
```
-D: ダンプ形式にする
-I: 空間インデックスを作成
-s: 座標系を定義（4326はespgコードで、WGS84）
`/work/data/pop_data/data/mesh1/mesh1.shp`はがインポートするshpファイル
`pop_mesh`は追加するテーブル名
`/work/data/pop_data/data/mesh1/mesh1.sql`は変換するsqlコマンドが記載されたファイル

#### 3.1.2. DBへの追加
1で作成したsqlコマンドを用いてgisdb DBへデータを追加する。

```sh
psql -U postgres -d gisdb -f /work/data/pop_data/data/mesh1/mesh1.sql
```

### 3.2. 人流データ(csv)のインポート
一月ごとの集計データが入手可能。
`prefs.zip`には、関東圏の1都6県の月別の人流データが格納されている。
この講義では負荷軽減のため2019年4月、2020年4月、2021年4月の集計データのみを使用する。

#### 3.2.1. gisdbにアクセス
```
psql -U postgres -d gisdb
```

#### 3.2.2. テーブル作成
```sql
CREATE TABLE "pop" (
    "mesh1kmid" varchar(80),
    "prefcode" varchar(80),
    "citycode" varchar(80),
    "year"  varchar(80),
    "month" varchar(80),
    "dayflag" varchar(80),
    "timezone" varchar(80),
    "population" numeric
);

```
テーブルを作成したらデータベースから抜ける。
```sql
\q
```
#### 3.2.3. csvデータのインポート
`pop_data`には1都6県の月別人流データが含まれている。
zipを解凍してcsvファイルを取り出し、かつpostgresqlにインポートするためのsqlコマンドを作成するshellスクリプト（`copy_csv.sh`）を作成し、`/work/data/pop_data`に配置する（すでにあるはず）。


```sh
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

```
作成したシェルを実行する．
```sh
sh /work/data/pop_data/copy_csv.sh
```

このシェルで作られた`copy_csv.sql`を実行してDBにデータをインポートする.
```sh
psql -U postgres -d gisdb -f /work/data/pop_data/copy_csv.sql
```

これですべてのでcsvデータが`pop`テーブルにインポートされる。

#### 3.2.4. meshとcsvデータの結合
定義書より、
集計期間(平休日) `dayflag`は“0”:休日 “1”:平日 “2”:全日
集計期間(時間帯) `timezone`は“0”:昼 “1”:深夜 “2”:終日
である。
ここでは2019年1月の休日・昼を考えてみよう。

以下をpsqlより実行して確認する。

```sh
psql -U postgres -d gisdb
```
```sql
SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom FROM pop AS d INNER JOIN pop_mesh AS p ON p.name = d.mesh1kmid WHERE d.dayflag='0' AND d.timezone='0' AND d.year='2019';

```

#### 3.2.5. レコード数のチェック
上記の問い合わせ処理のビューを作成してみる。
gisdbに接続した状態で、SQLで2020, 2021年のデータ休日昼間のviewを作成する。
 ```sql

CREATE VIEW pop201904 AS SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom FROM pop AS d INNER JOIN pop_mesh AS p ON p.name = d.mesh1kmid WHERE d.dayflag='0' AND d.timezone='0' AND d.year='2019';

CREATE VIEW pop202004 AS SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom FROM pop AS d INNER JOIN pop_mesh AS p ON p.name = d.mesh1kmid WHERE d.dayflag='0' AND d.timezone='0' AND d.year='2020';

CREATE VIEW pop202104 AS SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom FROM pop AS d INNER JOIN pop_mesh AS p ON p.name = d.mesh1kmid WHERE d.dayflag='0' AND d.timezone='0' AND d.year='2021';

```

```sql
select count(name) from pop_mesh;
select count(name) from pop201904;
select count(name) from pop202004;
select count(name) from pop202104;
```

## References
- 「全国の人流オープンデータ」（国土交通省）（https://www.geospatial.jp/ ckan/dataset/mlit-1km-fromto）
- （緊急事態宣言 1回目の状況」（NHK）(https://www3.nhk.or.jp/news/special/coronavirus/emergency/)
