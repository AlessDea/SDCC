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

# +-------------------------------------------------------------------------------------------------+
# | Circuit Breaker configurato con numero massimo di tentativi pari a 2 e timeout pari a 5 secondi |
# +-------------------------------------------------------------------------------------------------+
breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5, listeners=[GreetingsListener(), LogListener()])


# +---------------------------------------------------------------+
# | Invoca il microservizio Login per effettuare la registrazione |
# +---------------------------------------------------------------+
@breaker
def registration(username, password, isAgency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.registration(RegistrationRequest(username=username, password=password, isAgency=isAgency))
            return response.isRegistered
    except:
        raise Exception


# +-------------------------------------------------------+
# | Invoca il microservizio Login per effettuare il login |
# +-------------------------------------------------------+
@breaker
def doLogin(username, password, isAgency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.doLogin(LoginRequest(username=username, password=password, isAgency=isAgency))
            return response.isLogged
    except:
        raise Exception


# +------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio Login per controllare che un certo utente sia dipendete di una certa agenzia |
# +------------------------------------------------------------------------------------------------------+
@breaker
def checkEmployee(email, agency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.checkEmployee(CheckEmployeeRequest(email=email, agency=agency))
            return response.isEmployeeChecked
    except:
        raise Exception


# +------------------------------------------------------------------------------------------------+
# | Invoca il microservizio Login per inserire un certo utente come dipendete di una certa agenzia |
# +------------------------------------------------------------------------------------------------+
@breaker
def addEmployee(email, agency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.addEmployee(AddEmployeeRequest(email=email, agency=agency))
            return response.isEmployeeAdded
    except:
        raise Exception


# +----------------------------------------------------------------------------------------+
# | Invoca il microservizio Login per se una certa agenzia è registarata sulla piattaforma |
# +----------------------------------------------------------------------------------------+
@breaker
def checkAgency(agency):
    try:
        with grpc.insecure_channel('login-service:50052') as channel:
            stub = LoginStub(channel)
            response = stub.checkAgency(CheckAgencyRequest(agency=agency))
            return response.isAgencyChecked
    except:
        raise Exception


# +------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio NewPassword per generare una nuova password numerica e salvarla se richiesto |
# +------------------------------------------------------------------------------------------------------+
@breaker
def getNewNumericPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewNumericPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception


# +----------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio NewPassword per generare una nuova password alfanumerica e salvarla se richiesto |
# +----------------------------------------------------------------------------------------------------------+
@breaker
def getNewAlphaNumericPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewAlphaNumericPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception


# +--------------------------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio NewPassword per generare una nuova password con solo caratteri maiuscoli e salvarla se richiesto |
# +--------------------------------------------------------------------------------------------------------------------------+
@breaker
def getNewUpperPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewUpperPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception


# +--------------------------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio NewPassword per generare una nuova password con solo caratteri minuscoli e salvarla se richiesto |
# +--------------------------------------------------------------------------------------------------------------------------+
@breaker
def getNewLowerPassword(email, length, service, symbols, isSave):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewLowerPassword(NewPasswordRequest(email=email, length=length, service=service, symbols=symbols, hasToSave=isSave))
            return response.password, response.isSaved
    except:
        raise Exception


# +----------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio PasswordManager per salvare una nuova password o sovrascrivere una già esistente |
# +----------------------------------------------------------------------------------------------------------+
@breaker
def savePassword(email, password, service):
    try:
        with grpc.insecure_channel('managepw-service:50054') as channel:
            stub = SaverStub(channel)
            response = stub.SavePassword(SavePasswordRequest(email=email, password=password, service=service))
            return response.isStored
    except:
        raise Exception


# +---------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio PasswordManager per ricevere la lista delle password salvate di un certo utente |
# +---------------------------------------------------------------------------------------------------------+
@breaker
def doList(email):
    try:
        with grpc.insecure_channel('managepw-service:50054') as channel:
            stub = SaverStub(channel)
            response = stub.doList(ListPasswordRequest(email=email))
            return response.list
    except:
        raise Exception


# +-----------------------------------------------------------------+
# | Invoca il microservizio GroupManager per creare un buovo gruppo |
# +-----------------------------------------------------------------+
@breaker
def groupCreate(group_name, emails, agency):
    try:
        with grpc.insecure_channel('groupmanager-service:50057') as channel:
            stub = GroupManagerStub(channel)
            response = stub.groupCreate(GroupCreateRequest(group_name=group_name, emails=emails, agency=agency))
            return response.isCreated
    except:
        raise Exception


# +-------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio GroupManager per ricevere la lista dei gruppi di cui un certo utente fa parte |
# +-------------------------------------------------------------------------------------------------------+
@breaker
def groupList(email):
    try:
        with grpc.insecure_channel('groupmanager-service:50057') as channel:
            stub = GroupManagerStub(channel)
            response = stub.groupList(GroupListRequest(email=email))
            return response.list
    except:
        raise Exception


# +------------------------------------------------------------------------------+
# | Invoca il microservizio SharedPassword per richiedere una password condivisa |
# +------------------------------------------------------------------------------+
@breaker
def passwordRequest(group_name, email, service):
    try:
        with grpc.insecure_channel('sharedpw-service:50056') as channel:
            stub = SharedStub(channel)
            response = stub.passwordRequest(SharedPasswordRequest(group_name=group_name, email=email, service=service))
            return response.exists, response.password
    except Exception as e:
        raise e


# +---------------------------------------------------------------------------------------------+
# | Invoca il microservizio SharedPassword per verificare l'esistenza di una password condivisa |
# +---------------------------------------------------------------------------------------------+
@breaker
def checkPassword(group_name, agency, email, password):
    try:
        with grpc.insecure_channel('sharedpw-service:50056') as channel:
            stub = SharedStub(channel)
            response = stub.checkPassword(CheckSharedPasswordRequest(group_name=group_name, agency=agency, email=email, password=password))
            return response.isChecked
    except:
        raise Exception


# +------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio SharedPassword per accettare o declinare una richiesta di password condivisa |
# +------------------------------------------------------------------------------------------------------+
@breaker
def acceptDecline(group_name, service, email_applicant, email_member, token, accepted):
    try:
        with grpc.insecure_channel('sharedpw-service:50056') as channel:
            stub = SharedStub(channel)
            response = stub.acceptDecline(NotificationMessageRequest(group_name=group_name, service=service, email_applicant=email_applicant, email_member=email_member, token=token, accepted=accepted))
            return response.isOk
    except:
        raise Exception


# +------------------------------------------------------------------------------------------------------------------------------------+
# | Invoca il microservizio SharedPassword per ricevere la lista delle richieste di password condivisa che un certo utente ha ricevuto |
# +------------------------------------------------------------------------------------------------------------------------------------+
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