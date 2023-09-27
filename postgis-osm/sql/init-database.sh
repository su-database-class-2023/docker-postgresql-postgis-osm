#!/usr/bin/env bash

psql -U postgres -d postgre < "/docker-entrypoint-initdb.d/create-tables.sql"
psql -U postgres -d postgre < "/docker-entrypoint-initdb.d/insert-data.sql"