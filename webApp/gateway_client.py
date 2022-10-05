from __future__ import print_function

import random

import grpc
from protos.login_pb2 import *
from protos.login_pb2_grpc import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *
from protos.savepwd_pb2 import *
from protos.savepwd_pb2_grpc import *
from protos.register_pb2 import *
from protos.register_pb2_grpc import *
from protos.listing_pb2 import *
from protos.listing_pb2_grpc import *


def getNewNumPw(username, l, serv, sy, isSave):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewNumPass(PwRequest(name=username, length=l, service=serv, symbols=sy, hastoSave=isSave))
        return response.pw, response.isSaved


def getNewAlphNumPw(username, l, serv, sy, isSave):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewAlphaNumPass(PwRequest(name=username, length=l, service=serv, symbols=sy, hastoSave=isSave))
        return response.pw, response.isSaved


def getNewUpperPw(username, l, serv, sy, isSave):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewUpperPass(PwRequest(name=username, length=l, service=serv, symbols=sy, hastoSave=isSave))
        return response.pw, response.isSaved


def getNewLowerPw(username, l, serv, sy, isSave):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewLowerPass(PwRequest(name=username, length=l, service=serv, symbols=sy, hastoSave=isSave))
        return response.pw, response.isSaved


def doLogin(user, pssw, isAgency):
    with grpc.insecure_channel('login:50052') as channel:
        stub = LoginStub(channel)
        response = stub.doLogin(LogRequest(username=user, password=pssw, type=isAgency))
        return response.isLogged


def getEmail(user):
    with grpc.insecure_channel('login:50052') as channel:
        stub = LoginStub(channel)
        response = stub.getEmail(EmailRequest(username=user))
        return response.email


def registration(user, pssw, mail):
    with grpc.insecure_channel('register:50053') as channel:
        stub = RegisterStub(channel)
        response = stub.registration(RegRequest(username=user, password=pssw, email=mail))
        return response.isRegistered


def savePw(u, p, s):
    with grpc.insecure_channel('savepassword:50054') as channel:
        stub = SaverStub(channel)
        response = stub.SavePw(SaveRequest(username=u, pw=p, service=s))
        return response.isStored


def doList(u):
    with grpc.insecure_channel('listing:50055') as channel:
        stub = ListingStub(channel)
        response = stub.doList(ListRequest(username=u))
        return response.list
