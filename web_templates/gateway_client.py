from __future__ import print_function

import logging

import grpc
import newpassword_pb2
import newpassword_pb2_grpc



def  getNewPw(l):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewPass(newpassword_pb2.PwRequest(length=l))

        return response.pw


def getNewNumPw(l):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewNumPass(newpassword_pb2.PwRequest(length=l))

        return response.pw


def getNewAlphNumPw(l):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewAlphaNumPass(newpassword_pb2.PwRequest(length=l))

        return response.pw



