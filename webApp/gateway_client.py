from __future__ import print_function

import random

import grpc
import newpassword_pb2_grpc, newpassword_pb2
import savepwd_pb2, savepwd_pb2_grpc
import login_pb2_grpc, login_pb2


def getNewNumPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewNumPass(newpassword_pb2.PwRequest(length=l, symbols=sy))

        return response.pw


def getNewAlphNumPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewAlphaNumPass(newpassword_pb2.PwRequest(length=l, symbols=sy))

        return response.pw


def getNewUpperPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewUpperPass(newpassword_pb2.PwRequest(length=l, symbols=sy))

        return response.pw


def getNewLowerPw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewLowerPass(newpassword_pb2.PwRequest(length=l, symbols=sy))

        return response.pw


def savePw(u, p, s):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = savepwd_pb2_grpc.SaverStub(channel)
        response = stub.SavePw(savepwd_pb2.SaveRequest(username=u, pw=p, service=s))

        return response

def doLogin(user, pssw):
    with grpc.insecure_channel('login:50052') as channel:
        stub = login_pb2_grpc.LoginStub(channel)
        response = stub.doLogin(login_pb2.PwRequest(username=user, password=pssw))
        return response.isLogged
