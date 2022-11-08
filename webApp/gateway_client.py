import grpc

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
from protos.notification_pb2 import *
from protos.notification_pb2_grpc import *


def registration(username, password, isAgency):
    with grpc.insecure_channel('login-service:50052') as channel:
        stub = LoginStub(channel)
        response = stub.registration(RegistrationRequest(username=username, password=password, isAgency=isAgency))
        return response.isRegistered


def doLogin(username, password, isAgency):
    with grpc.insecure_channel('login-service:50052') as channel:
        stub = LoginStub(channel)
        response = stub.doLogin(LoginRequest(username=username, password=password, isAgency=isAgency))
        return response.isLogged


def checkEmployee(email, agency):
    with grpc.insecure_channel('login-service:50052') as channel:
        stub = LoginStub(channel)
        response = stub.checkEmployee(CheckEmployeeRequest(email=email, agency=agency))
        return response.isEmployeeChecked


def addEmployee(email, agency):
    with grpc.insecure_channel('login-service:50052') as channel:
        stub = LoginStub(channel)
        response = stub.addEmployee(AddEmployeeRequest(email=email, agency=agency))
        return response.isEmployeeAdded


def checkAgency(agency):
    with grpc.insecure_channel('login-service:50052') as channel:
        stub = LoginStub(channel)
        response = stub.checkAgency(CheckAgencyRequest(agency=agency))
        return response.isAgencyChecked


def getNewNumericPassword(email, length, service, symbols, isSave):
    with grpc.insecure_channel('newpw-service:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewNumericPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
        return response.password, response.isSaved


def getNewAlphaNumericPassword(email, length, service, symbols, isSave):
    with grpc.insecure_channel('newpw-service:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewAlphaNumericPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
        return response.password, response.isSaved


def getNewUpperPassword(email, length, service, symbols, isSave):
    with grpc.insecure_channel('newpw-service:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewUpperPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
        return response.password, response.isSaved


def getNewLowerPassword(email, length, service, symbols, isSave):
    with grpc.insecure_channel('newpw-service:50051') as channel:
        stub = PasswordStub(channel)
        response = stub.GetNewLowerPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
        return response.password, response.isSaved


def savePassword(email, password, service):
    with grpc.insecure_channel('managepw-service:50054') as channel:
        stub = SaverStub(channel)
        response = stub.SavePassword(SavePasswordRequest(email=email, password=password, service=service))
        return response.isStored


def doList(email):
    with grpc.insecure_channel('managepw-service:50054') as channel:
        stub = SaverStub(channel)
        response = stub.doList(ListPasswordRequest(email=email))
        return response.list


def groupCreate(group_name, emails, agency):
    with grpc.insecure_channel('groupmanager-service:50057') as channel:
        stub = GroupManagerStub(channel)
        response = stub.groupCreate(GroupCreateRequest(group_name=group_name, emails=emails, agency=agency))
        return response.isCreated


def groupList(email):
    with grpc.insecure_channel('groupmanager-service:50057') as channel:
        stub = GroupManagerStub(channel)
        response = stub.groupList(GroupListRequest(email=email))
        return response.list


def passwordRequest(group_name, email, service):
    with grpc.insecure_channel('sharedpw-service:50056') as channel:
        stub = SharedStub(channel)
        response = stub.passwordRequest(SharedPasswordRequest(group_name=group_name, email=email, service=service))
        return response.exists, response.password


def checkPassword(group_name, agency, email, password):
    with grpc.insecure_channel('sharedpw-service:50056') as channel:
        stub = SharedStub(channel)
        response = stub.checkPassword(CheckSharedPasswordRequest(group_name=group_name, agency=agency, email=email, password=password))
        return response.isChecked


def checkStatus(group_name, email, service):
    with grpc.insecure_channel('notification-service:50058') as channel:
        stub = NotificationStub(channel)
        response = stub.checkStatus(CheckStatusRequest(group_name=group_name, email=email, service=service))
        return response.status, response.total


def acceptDecline(group_name, service, email_applicant, email_member, token, accepted):
    with grpc.insecure_channel('notification-service:50058') as channel:
        stub = NotificationStub(channel)
        response = stub.acceptDecline(NotificationMessageRequest(group_name=group_name, service=service, email_applicant=email_applicant, email_member=email_member, token=token, accepted=accepted))
        return response.isOk