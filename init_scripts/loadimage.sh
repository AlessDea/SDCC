#!/bin/sh
echo "Start deleting old images..."
minikube image rm webapp-image 2>/dev/null
minikube image rm restgateway-image 2>/dev/null
minikube image rm doubleauth-image 2>/dev/null
minikube image rm groupmanager-image 2>/dev/null
minikube image rm login-image 2>/dev/null
minikube image rm managepw-image 2>/dev/null
minikube image rm newpw-image 2>/dev/null
minikube image rm notification-image 2>/dev/null
minikube image rm sharedpw-image 2>/dev/null
echo "Finish deleting old images"
echo "Start loading images..."
echo "Start loading webapp-image..."
minikube image load webapp-image
echo "webapp-image loaded"
echo "Start loading restgateway-image..."
minikube image load restgateway-image
echo "restgateway-image loaded"
echo "Start loading doubleauth-image..."
minikube image load doubleauth-image
echo "doubleauth-image loaded"
echo "Start loading groupmanager-image..."
minikube image load groupmanager-image
echo "groupmanager-image loaded"
echo "Start loading login-image..."
minikube image load login-image
echo "login-image loaded"
echo "Start loading managepw-image..."
minikube image load managepw-image
echo "managepw-image loaded"
echo "Start loading newpw-image..."
minikube image load newpw-image
echo "newpw-image loaded"
echo "Start loading notification-image..."
minikube image load notification-image
echo "notification-image loaded"
echo "Start loading sharedpw-image..."
minikube image load sharedpw-image
echo "sharedpw-image loaded"
echo "Finish loading images"