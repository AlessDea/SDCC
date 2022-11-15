# creazione di password sicura:
# 	- lunghezza (min lunghezza max)
#	- tipo: num, alfanum, solo lettere
#	- simboli speciali
#	- upper lowercase
#	- parola chiave (non consigliato)

import random
import os
import pickle

from concurrent import futures
import logging
import grpc
from flask import flash

from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *
from protos.managepassword_pb2 import *
from protos.managepassword_pb2_grpc import *

from lib.breaker_listeners import *

breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5, listeners=[GreetingsListener(), LogListener()])


alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetLower = 'abcdefghijklmnopqrstuvwxyz'
alphabetDigits = '0123456789'
alphabetPunctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
alphabetComplete = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

perc = 0.3


def generate_num_code(l, sy):
    code = ''

    for _ in range(l):
        if sy == True:
            if random.random() <= 0.3:
                code += random.choice(alphabetPunctuation)
            else:
                code += random.choice(alphabetDigits)

        else:
            code += random.choice(alphabetDigits)

    with open('state.dat', 'wb') as f:
        pickle.dump(random.getstate(), f)

    return code


def generate_lower_code(l, sy):
    code = ''

    for _ in range(l):
        if sy == True:
            if random.random() <= 0.3:
                code += random.choice(alphabetPunctuation)
            else:
                code += random.choice(alphabetLower + alphabetDigits)

        else:
            code += random.choice(alphabetLower + alphabetDigits)

    with open('state.dat', 'wb') as f:
        pickle.dump(random.getstate(), f)

    return code


def generate_upper_code(l, sy):
    code = ''

    for _ in range(l):
        if sy == True:
            if random.random() <= 0.3:
                code += random.choice(alphabetPunctuation)
            else:
                code += random.choice(alphabetUpper + alphabetDigits)

        else:
            code += random.choice(alphabetUpper + alphabetDigits)

    with open('state.dat', 'wb') as f:
        pickle.dump(random.getstate(), f)

    return code


def generate_alphanumeric_code(l, sy):
    code = ''

    for _ in range(l):
        if sy == True:
            if random.random() <= 0.3:
                code += random.choice(alphabetPunctuation)
            else:
                code += random.choice(alphabetUpper + alphabetLower + alphabetDigits)
        else:
            code += random.choice(alphabetUpper + alphabetLower + alphabetDigits)

    with open('state.dat', 'wb') as f:
        pickle.dump(random.getstate(), f)

    return code


def checkRandomStatus():
    if os.path.exists('state.dat'):
        # Restore the previously saved state
        #print('Found state.dat, initializing random module')
        with open('state.dat', 'rb') as f:
            state = pickle.load(f)
        random.setstate(state)
    else:
        # Use a well-known start state
        #print('No state.dat, seeding')
        random.seed(12345)

@breaker
def savePassword(email, password, service):
    try:
        with grpc.insecure_channel('managepw-service:50054') as channel:
            stub = SaverStub(channel)
            response = stub.SavePassword(SavePasswordRequest(email=email, password=password, service=service))
            return response.isStored
    except:
        raise Exception


class Password(PasswordServicer):

    def GetNewNumericPassword(self, request, context):
        npw = generate_num_code(request.length, request.symbols)
        isStored = False
        if request.hasToSave:
            try:
                isStored = savePassword(request.email, npw, request.service)
            except:
                raise Exception
        return NewPasswordReply(password=npw, isSaved=isStored)

    def GetNewLowerPassword(self, request, context):
        npw = generate_lower_code(request.length, request.symbols)
        isStored = False
        if request.hasToSave:
            try:
                isStored = savePassword(request.email, npw, request.service)
            except:
                raise Exception
        return NewPasswordReply(password=npw, isSaved=isStored)

    def GetNewUpperPassword(self, request, context):
        npw = generate_upper_code(request.length, request.symbols)
        isStored = False
        if request.hasToSave:
            try:
                isStored = savePassword(request.email, npw, request.service)
            except:
                raise Exception
        return NewPasswordReply(password=npw, isSaved=isStored)

    def GetNewAlphaNumericPassword(self, request, context):
        npw = generate_alphanumeric_code(request.length, request.symbols)
        isStored = False
        if request.hasToSave:
            try:
                isStored = savePassword(request.email, npw, request.service)
            except:
                raise Exception
        return NewPasswordReply(password=npw, isSaved=isStored)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PasswordServicer_to_server(Password(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    checkRandomStatus()
    logging.basicConfig()
    serve()