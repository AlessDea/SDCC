#!/bin/sh
docker build -t webapp-image ../webApp/clientgateway/.
docker build -t restgateway-image ../webApp/restgateway/.
docker build -t doubleauth-image ../services/doubleauth/.
docker build -t groupmanager-image ../services/groupmanager/.
docker build -t login-image ../services/login/.
docker build -t managepw-image ../services/managepw/.
docker build -t newpw-image ../services/newpw/.
docker build -t notification-image ../services/notification/.
docker build -t sharedpw-image ../services/sharedpw/.
echo "y" | docker system prune 