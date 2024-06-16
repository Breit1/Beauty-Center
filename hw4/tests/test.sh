#!/bin/bash

export PG_HOST=127.0.0.1
export PG_PORT=5432
export PG_USER=test
export PG_PASSWORD=test
export PG_DBNAME=postgres
export SECRET_KEY='*(%yyrvtlt-=6s*foyy5xcbo@!@b73a@m-g$bs_ek%s$d!sbl@'

python manage.py test $1