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


def getNewNumPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewNumPass(PwRequest(length=l, symbols=sy))

        return response.pw


def getNewAlphNumPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewAlphaNumPass(PwRequest(length=l, symbols=sy))

        return response.pw


def getNewUpperPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewUpperPass(PwRequest(length=l, symbols=sy))

        return response.pw


def getNewLowerPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewLowerPass(PwRequest(length=l, symbols=sy))

        return response.pw


def savePw(u, p, s):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = SaverStub(channel)
        response = stub.SavePw(SaveRequest(username=u, pw=p, service=s))

        return response

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
