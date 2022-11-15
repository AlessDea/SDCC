import grpc
import logging

from protos.login_pb2_grpc import *
from protos.login_pb2 import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *
from protos.managepassword_pb2 import *
from protos.managepassword_pb2_grpc import *
from protos.groupmanager_pb2 import *
from protos.groupmanager_pb2_grpc import *
from protos.sharedpw_pb2 import *
from protos.sharedpw_pb2_grpc import *

from lib.breaker_listeners import *

breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5, listeners=[GreetingsListener(), LogListener()])


@breaker
def registration(username, password, isAgency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.registration(RegistrationRequest(username=username, password=password, isAgency=isAgency))
            return response.isRegistered
    except:
        raise Exception

@breaker
def doLogin(username, password, isAgency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.doLogin(LoginRequest(username=username, password=password, isAgency=isAgency))
            return response.isLogged
    except:
        raise Exception

@breaker
def checkEmployee(email, agency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.checkEmployee(CheckEmployeeRequest(email=email, agency=agency))
            return response.isEmployeeChecked
    except:
        raise Exception

@breaker
def addEmployee(email, agency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.addEmployee(AddEmployeeRequest(email=email, agency=agency))
            return response.isEmployeeAdded
    except:
        raise Exception

@breaker
def checkAgency(agency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.checkAgency(CheckAgencyRequest(agency=agency))
            return response.isAgencyChecked
    except:
        raise Exception

@breaker
def getNewNumericPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewNumericPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception

@breaker
def getNewAlphaNumericPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewAlphaNumericPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception

@breaker
def getNewUpperPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewUpperPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception

@breaker
def getNewLowerPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewLowerPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception

@breaker
def savePassword(email, password, service):
    try:
        with grpc.insecure_channel('managepw-service:50054') as channel:
            stub = SaverStub(channel)
            response = stub.SavePassword(SavePasswordRequest(email=email, password=password, service=service))
            return response.isStored
    except:
        raise Exception

@breaker
def doList(email):
    try:
        with grpc.insecure_channel('managepw-service:50054') as channel:
            stub = SaverStub(channel)
            response = stub.doList(ListPasswordRequest(email=email))
            return response.list
    except:
        raise Exception

@breaker
def groupCreate(group_name, emails, agency):
    try:
        with grpc.insecure_channel('groupmanager-service:50057') as channel:
            stub = GroupManagerStub(channel)
            response = stub.groupCreate(GroupCreateRequest(group_name=group_name, emails=emails, agency=agency))
            return response.isCreated
    except:
        raise Exception

@breaker
def groupList(email):
    try:
        with grpc.insecure_channel('groupmanager-service:50057') as channel:
            stub = GroupManagerStub(channel)
            response = stub.groupList(GroupListRequest(email=email))
            return response.list
    except:
        raise Exception

@breaker
def passwordRequest(group_name, email, service):
    try:
        with grpc.insecure_channel('sharedpw-service:50056') as channel:
            stub = SharedStub(channel)
            response = stub.passwordRequest(SharedPasswordRequest(group_name=group_name, email=email, service=service))
            return response.exists, response.password
    except Exception as e:
        raise e

@breaker
def checkPassword(group_name, agency, email, password):
    try:
        with grpc.insecure_channel('sharedpw-service:50056') as channel:
            stub = SharedStub(channel)
            response = stub.checkPassword(CheckSharedPasswordRequest(group_name=group_name, agency=agency, email=email, password=password))
            return response.isChecked
    except:
        raise Exception

@breaker
def acceptDecline(group_name, service, email_applicant, email_member, token, accepted):
    try:
        with grpc.insecure_channel('sharedpw-service:50056') as channel:
            stub = SharedStub(channel)
            response = stub.acceptDecline(NotificationMessageRequest(group_name=group_name, service=service, email_applicant=email_applicant, email_member=email_member, token=token, accepted=accepted))
            return response.isOk
    except:
        raise Exception

@breaker
def getRequestList(email):
    try:
        with grpc.insecure_channel('sharedpw-service:50056') as channel:
            stub = SharedStub(channel)
            response = stub.getRequestList(GetListRequest(email=email))
            logging.warning('Response.lista: ' + str(response.lista))
            lista = []
            for i in range(len(response.lista)):
                lista.append([response.lista[i].agency, response.lista[i].group_name, response.lista[i].applicant])
            return lista
    except Exception as e:
        logging.warning('GetList Gateway exception: ' + str(e))
        raise Exception