#!/bin/bash
podman build -f Dockerfile --build-arg USER_ID=1000 --build-arg GROUP_ID=1000 -t gapapp-v0.2