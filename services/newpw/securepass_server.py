# creazione di password sicura:
# 	- lunghezza (min lunghezza max)
#	- tipo: num, alfanum, solo lettere
#	- simboli speciali
#	- upper lowercase
#	- parola chiave (non consigliato)

import string
import random
import os
import pickle

from concurrent import futures
import logging
import grpc
import newpassword_pb2
import newpassword_pb2_grpc

alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetLower = 'abcdefghijklmnopqrstuvwxyz'
alphabetDigits = '0123456789'
alphabetPunctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
alphabetComplete = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


perc = 0.3

def generate_num_code(l, sy):
    code = ''

    for j in range(l):
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

    for j in range(l):
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

    for j in range(l):
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


# no symbols
def generate_alphanumeric_code(l, sy):
    code = ''

    for j in range(l):
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


class Password(newpassword_pb2_grpc.PasswordServicer):


    def GetNewNumPass(self, request, context):
        npw = generate_num_code(request.length, request.symbols)
        return newpassword_pb2.PwReply(message='la tua password: ', pw=npw)

    def GetNewLowerPass(self, request, context):
        npw = generate_lower_code(request.length, request.symbols)
        return newpassword_pb2.PwReply(message='la tua password: ', pw=npw)

    def GetNewUpperPass(self, request, context):
        npw = generate_upper_code(request.length, request.symbols)
        return newpassword_pb2.PwReply(message='la tua password: ', pw=npw)

# no symbols
    def GetNewAlphaNumPass(self, request, context):
        npw = generate_alphanumeric_code(request.length, request.symbols)
        return newpassword_pb2.PwReply(message='la tua password: ', pw=npw)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    newpassword_pb2_grpc.add_PasswordServicer_to_server(Password(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    checkRandomStatus()
    logging.basicConfig()
    serve()