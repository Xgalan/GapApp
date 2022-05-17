#!/bin/bash
# build command for docker image
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
docker-compose build
