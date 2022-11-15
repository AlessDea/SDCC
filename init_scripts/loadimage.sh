#!/bin/sh
minikube image load webapp-image
echo "webapp-image loaded"
minikube image load restgateway-image
echo "restgateway-image loaded"
minikube image load doubleauth-image
echo "doubleauth-image loaded"
minikube image load groupmanager-image
echo "groupmanager-image loaded"
minikube image load login-image
echo "login-image loaded"
minikube image load managepw-image
echo "managepw-image loaded"
minikube image load newpw-image
echo "newpw-image loaded"
minikube image load notification-image
echo "notification-image loaded"
minikube image load sharedpw-image
echo "sharedpw-image loaded"