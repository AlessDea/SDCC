#!/bin/sh
kubectl apply -f ./doubleauth/.
kubectl apply -f ./groupmanager/.
kubectl apply -f ./login/.
kubectl apply -f ./managepw/.
kubectl apply -f ./newpw/.
kubectl apply -f ./notification/.
kubectl apply -f ./sharedpw/.