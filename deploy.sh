#!/bin/bash
export HOST_IP=<hostip>
# Remove Hardcoding from above and below
cd /home/ubuntu/microservice
docker-compose scale gitchangelogservice=0
docker rm $(docker ps -q -f status=exited)
docker rmi -f swiftops/ms-gitchangelog && docker pull swiftops/ms-gitchangelog && docker-compose up -d --remove-orphans