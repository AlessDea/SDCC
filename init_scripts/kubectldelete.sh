#!/bin/sh
kubectl delete -f ../webApp/restgateway/.
kubectl delete -f ../services/doubleauth/.
kubectl delete -f ../services/groupmanager/.
kubectl delete -f ../services/login/.
kubectl delete -f ../services/managepw/.
kubectl delete -f ../webApp/clientgateway/.
kubectl delete -f ../services/newpw/.
kubectl delete -f ../services/notification/.
kubectl delete -f ../services/sharedpw/.