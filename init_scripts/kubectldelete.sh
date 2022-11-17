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