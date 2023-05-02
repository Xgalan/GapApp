#!/bin/bash
source .env.podman
podman create --replace --name gapapp-v0.2 \
--env-file=./gap/.env \
-u root --userns=keep-id --group-add=keep-groups \
-v=gapapp_vol:/usr/src/app:Z \
-v=$DATABASE_DIR:/srv/databases:Z \
--network=slirp4netns:allow_host_loopback=true \
-p=$CT_PORT:8000 \
gapapp-v0.2:latest \
gunicorn --worker-tmp-dir /dev/shm --config ./gap/gunicorn.conf.py gap.wsgi:application
