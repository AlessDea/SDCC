#!/bin/sh
kubectl delete -f ../webApp/restgateway/. 2>/dev/null
kubectl delete -f ../services/doubleauth/. 2>/dev/null
kubectl delete -f ../services/groupmanager/. 2>/dev/null
kubectl delete -f ../services/login/. 2>/dev/null
kubectl delete -f ../services/managepw/. 2>/dev/null
kubectl delete -f ../webApp/clientgateway/. 2>/dev/null
kubectl delete -f ../services/newpw/. 2>/dev/null
kubectl delete -f ../services/notification/. 2>/dev/null
kubectl delete -f ../services/sharedpw/. 2>/dev/null
echo "Start applying yaml..."
kubectl apply -f ../webApp/clientgateway/.
kubectl apply -f ../webApp/restgateway/.
kubectl apply -f ../services/doubleauth/.
kubectl apply -f ../services/groupmanager/.
kubectl apply -f ../services/login/.
kubectl apply -f ../services/managepw/.
kubectl apply -f ../services/newpw/.
kubectl apply -f ../services/notification/.
kubectl apply -f ../services/sharedpw/.
echo "Finish applying yaml"