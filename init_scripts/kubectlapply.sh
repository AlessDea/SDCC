#!/bin/sh
kubectl apply -f ../webApp/clientgateway/.
kubectl apply -f ../webApp/restgateway/.
kubectl apply -f ../services/doubleauth/.
kubectl apply -f ../services/groupmanager/.
kubectl apply -f ../services/login/.
kubectl apply -f ../services/managepw/.
kubectl apply -f ../services/newpw/.
kubectl apply -f ../services/notification/.
kubectl apply -f ../services/sharedpw/.