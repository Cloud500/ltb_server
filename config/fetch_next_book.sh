#!/bin/sh

generate_post_data()
{
   cat <<EOF
{
  "user": "$CRON_USER",
  "password": "$CRON_PASSWORD"
}
EOF
}

curl -X POST http://localhost:8000/api/v1/fetch_new_books -H 'Content-Type: application/json' -d "$(generate_post_data)"