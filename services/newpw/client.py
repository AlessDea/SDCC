from __future__ import print_function

import logging

import grpc
import newpassword_pb2
import newpassword_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = newpassword_pb2_grpc.PasswordStub(channel)
        response = stub.GetNewPass(newpassword_pb2.PwRequest(name='Alessandro', length=10))
        print("Response: " + response.message +response.pw)


if __name__ == '__main__':
    logging.basicConfig()
    run()
