from __future__ import print_function

import logging
import random

import grpc
import newpassword_pb2
import newpassword_pb2_grpc




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


def savePw(l, sy):
    with grpc.insecure_channel('newpassword:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        #response = stub.GetNewLowerPass(newpassword_pb2.PwRequest(length=l, symbols=sy))
        if random.random() <= 0.5:
            return True
        return False


