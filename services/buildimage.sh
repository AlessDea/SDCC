#!/bin/sh
docker build -t doubleauth-image ./doubleauth/.
docker build -t groupmanager-image ./groupmanager/.
docker build -t login-image ./login/.
docker build -t managepw-image ./managepw/.
docker build -t newpw-image ./newpw/.
docker build -t notification-image ./notification/.
docker build -t sharedpw-image ./sharedpw/.
echo "y" | docker system prune 