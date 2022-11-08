# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos.login_pb2 as login__pb2


class LoginStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.registration = channel.unary_unary(
                '/login.Login/registration',
                request_serializer=login__pb2.RegistrationRequest.SerializeToString,
                response_deserializer=login__pb2.RegistrationReply.FromString,
                )
        self.doLogin = channel.unary_unary(
                '/login.Login/doLogin',
                request_serializer=login__pb2.LoginRequest.SerializeToString,
                response_deserializer=login__pb2.LoginReply.FromString,
                )
        self.checkEmployee = channel.unary_unary(
                '/login.Login/checkEmployee',
                request_serializer=login__pb2.CheckEmployeeRequest.SerializeToString,
                response_deserializer=login__pb2.CheckEmployeeReply.FromString,
                )
        self.addEmployee = channel.unary_unary(
                '/login.Login/addEmployee',
                request_serializer=login__pb2.AddEmployeeRequest.SerializeToString,
                response_deserializer=login__pb2.AddEmployeeReply.FromString,
                )
        self.checkAgency = channel.unary_unary(
                '/login.Login/checkAgency',
                request_serializer=login__pb2.CheckAgencyRequest.SerializeToString,
                response_deserializer=login__pb2.CheckAgencyReply.FromString,
                )


class LoginServicer(object):
    """Missing associated documentation comment in .proto file."""

    def registration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doLogin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkEmployee(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addEmployee(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkAgency(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LoginServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'registration': grpc.unary_unary_rpc_method_handler(
                    servicer.registration,
                    request_deserializer=login__pb2.RegistrationRequest.FromString,
                    response_serializer=login__pb2.RegistrationReply.SerializeToString,
            ),
            'doLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.doLogin,
                    request_deserializer=login__pb2.LoginRequest.FromString,
                    response_serializer=login__pb2.LoginReply.SerializeToString,
            ),
            'checkEmployee': grpc.unary_unary_rpc_method_handler(
                    servicer.checkEmployee,
                    request_deserializer=login__pb2.CheckEmployeeRequest.FromString,
                    response_serializer=login__pb2.CheckEmployeeReply.SerializeToString,
            ),
            'addEmployee': grpc.unary_unary_rpc_method_handler(
                    servicer.addEmployee,
                    request_deserializer=login__pb2.AddEmployeeRequest.FromString,
                    response_serializer=login__pb2.AddEmployeeReply.SerializeToString,
            ),
            'checkAgency': grpc.unary_unary_rpc_method_handler(
                    servicer.checkAgency,
                    request_deserializer=login__pb2.CheckAgencyRequest.FromString,
                    response_serializer=login__pb2.CheckAgencyReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'login.Login', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Login(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def registration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/login.Login/registration',
            login__pb2.RegistrationRequest.SerializeToString,
            login__pb2.RegistrationReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def doLogin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/login.Login/doLogin',
            login__pb2.LoginRequest.SerializeToString,
            login__pb2.LoginReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkEmployee(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/login.Login/checkEmployee',
            login__pb2.CheckEmployeeRequest.SerializeToString,
            login__pb2.CheckEmployeeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addEmployee(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/login.Login/addEmployee',
            login__pb2.AddEmployeeRequest.SerializeToString,
            login__pb2.AddEmployeeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkAgency(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/login.Login/checkAgency',
            login__pb2.CheckAgencyRequest.SerializeToString,
            login__pb2.CheckAgencyReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
