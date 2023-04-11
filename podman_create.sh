#!/bin/bash
podman create --replace --name gapapp-v0.2 \
--env-file=./gap/.env \
--userns=keep-id --group-add=keep-groups \
-v gapapp_vol:/usr/src/app \
--network=slirp4netns:allow_host_loopback=true \
-p=8080:8080 \
gapapp-v0.2:latest \
gunicorn --worker-tmp-dir /dev/shm --config ./gap/gunicorn.conf.py gap.wsgi:application