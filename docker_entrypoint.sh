#!/bin/sh
printenv | sed 's/^\(.*\)$/export \1/g' > /banktransactioncollect/project_env.sh
chmod +x /banktransactioncollect/project_env.sh
cron -f
