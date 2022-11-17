# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos.doubleauth_pb2 as doubleauth__pb2


class DoubleauthStub(object):
    """The  service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.doLoginThirdPart = channel.unary_unary(
                '/newpw.Doubleauth/doLoginThirdPart',
                request_serializer=doubleauth__pb2.GenCodeRequest.SerializeToString,
                response_deserializer=doubleauth__pb2.Reply.FromString,
                )
        self.checkCode = channel.unary_unary(
                '/newpw.Doubleauth/checkCode',
                request_serializer=doubleauth__pb2.CheckCodeRequest.SerializeToString,
                response_deserializer=doubleauth__pb2.Reply.FromString,
                )
        self.registrationThirdPart = channel.unary_unary(
                '/newpw.Doubleauth/registrationThirdPart',
                request_serializer=doubleauth__pb2.RegistrationRequest.SerializeToString,
                response_deserializer=doubleauth__pb2.Reply.FromString,
                )


class DoubleauthServicer(object):
    """The  service definition.
    """

    def doLoginThirdPart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkCode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registrationThirdPart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DoubleauthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'doLoginThirdPart': grpc.unary_unary_rpc_method_handler(
                    servicer.doLoginThirdPart,
                    request_deserializer=doubleauth__pb2.GenCodeRequest.FromString,
                    response_serializer=doubleauth__pb2.Reply.SerializeToString,
            ),
            'checkCode': grpc.unary_unary_rpc_method_handler(
                    servicer.checkCode,
                    request_deserializer=doubleauth__pb2.CheckCodeRequest.FromString,
                    response_serializer=doubleauth__pb2.Reply.SerializeToString,
            ),
            'registrationThirdPart': grpc.unary_unary_rpc_method_handler(
                    servicer.registrationThirdPart,
                    request_deserializer=doubleauth__pb2.RegistrationRequest.FromString,
                    response_serializer=doubleauth__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'newpw.Doubleauth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Doubleauth(object):
    """The  service definition.
    """

    @staticmethod
    def doLoginThirdPart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Doubleauth/doLoginThirdPart',
            doubleauth__pb2.GenCodeRequest.SerializeToString,
            doubleauth__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkCode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Doubleauth/checkCode',
            doubleauth__pb2.CheckCodeRequest.SerializeToString,
            doubleauth__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def registrationThirdPart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Doubleauth/registrationThirdPart',
            doubleauth__pb2.RegistrationRequest.SerializeToString,
            doubleauth__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)