#!/usr/bin/env bash

psql -U postgres -d postgre < "/sql/dvdrental_create-table.sql"
pg_restore -U postgres -d dvdrental /sample/dvdrental.tar