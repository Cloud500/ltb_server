#!/bin/sh

curl -X POST http://localhost:8000/api/v1/fetch_new_books -H 'Content-Type: application/json' -d '{"user":"$CRON_USER","password":"$CRON_PASSWORD"}'
