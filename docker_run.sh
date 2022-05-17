#!/bin/bash
# start stack
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
docker-compose up -d