from flask import Flask, request
from flask_restful import Api, Resource
import json
import logging

from protos.doubleauth_pb2_grpc import *
from protos.doubleauth_pb2 import *
from protos.sharedpw_pb2_grpc import *
from protos.sharedpw_pb2 import *

app = Flask(__name__)
api = Api(app)


def check_shared(arg):
	# grpc request to SharedPw microservice
	try:
		with grpc.insecure_channel('sharedpw-service:50056') as channel:
			stub = SharedStub(channel)
			response = stub.checkPassword(CheckSharedPasswordRequest(group_name=arg['group_name'], email=arg['email'], agency=arg['service'], password=arg['password']))
			return response.isChecked
	except:
		return False


def gen_double_code(arg):
	try:
		with grpc.insecure_channel('doubleauth-service:50059') as channel:
			stub = DoubleauthStub(channel)
			response = stub.doLoginThirdPart(
				GenCodeRequest(email=arg['email'], service=arg['service']))
			return response.message
	except:
		return False


def check_double_code(arg):
	#print('Check Double Code - ' + str(arg['email']) + str(arg['service']) + str(arg['code']))
	logging.warning('Check Double Code - ' + str(arg['email']) + str(arg['service']) + str(arg['code']))
	try:
		with grpc.insecure_channel('doubleauth-service:50059') as channel:
			stub = DoubleauthStub(channel)
			response = stub.checkCode(CheckCodeRequest(email=arg['email'], service=arg['service'], code=arg['code']))
			#print('Check Double Code - Try: ' + str(response.message))
			logging.warning('Check Double Code - Try: ' + str(response.message))
			return response.message
	except:
		logging.warning('Check Double Code - Except')
		#print('Check Double Code - Except')
		return False


def reg_user_double(arg):
	try:
		with grpc.insecure_channel('doubleauth-service:50059') as channel:
			stub = DoubleauthStub(channel)
			response = stub.registrationThirdPart(
				RegistrationRequest(email=arg['email'], service=arg['service']))
			return response.message
	except:
		return False


class SharedPw(Resource):
	def post(self):
		req = json.loads(request.get_json())
		if check_shared(req):
			return { "Answer": "OK" }
		else:
			return {"Answer": "DECLINE"}

		
class DoubleAuth(Resource):

	def post(self):
		req = json.loads(request.get_json())
		if(check_double_code(req)):
			return {"Answer": "CORRECT"}
		else:
			return {"Answer": "ERROR"}

	def put(self):
		req = json.loads(request.get_json())
		if (gen_double_code(req)):
			return {"Answer": "OK"}
		else:
			return {"Answer": "ERROR"}


class RegisterUser(Resource):

	def put(self):
		req = json.loads(request.get_json())
		if reg_user_double(req):
			return { "Answer": "REGISTERED" }
		else:
			return {"Answer": "DECLINE"}

# APIs
api.add_resource(SharedPw, '/shared_pass')
api.add_resource(DoubleAuth, '/double_auth')
api.add_resource(RegisterUser, '/register_user')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)