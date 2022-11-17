#!/bin/sh
echo "Start building images..."
docker image rmi webapp-image 2>/dev/null
docker image rmi restgateway-image 2>/dev/null
docker image rmi doubleauth-image 2>/dev/null
docker image rmi groupmanager-image 2>/dev/null
docker image rmi login-image 2>/dev/null
docker image rmi managepw-image 2>/dev/null
docker image rmi newpw-image 2>/dev/null
docker image rmi notification-image 2>/dev/null
docker image rmi sharedpw-image 2>/dev/null
docker build -t webapp-image ../webApp/clientgateway/.
docker build -t restgateway-image ../webApp/restgateway/.
docker build -t doubleauth-image ../services/doubleauth/.
docker build -t groupmanager-image ../services/groupmanager/.
docker build -t login-image ../services/login/.
docker build -t managepw-image ../services/managepw/.
docker build -t newpw-image ../services/newpw/.
docker build -t notification-image ../services/notification/.
docker build -t sharedpw-image ../services/sharedpw/.
echo "Finish building images"