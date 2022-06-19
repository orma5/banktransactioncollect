#!/bin/sh
printenv | sed 's/^\(.*\)$/export \1/g' > /root/project_env.sh
chmod +x /root/project_env.sh
cron -f
