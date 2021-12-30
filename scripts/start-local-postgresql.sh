#!/bin/bash

sudo -i -u postgres bash << EOF
pg_ctl start -D /Library/PostgreSQL/14/data/
EOF
echo "Started"