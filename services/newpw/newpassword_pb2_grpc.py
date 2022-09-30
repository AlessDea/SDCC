# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import newpassword_pb2 as newpassword__pb2


class PasswordStub(object):
    """The  service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetNewPass = channel.unary_unary(
                '/newpw.Password/GetNewPass',
                request_serializer=newpassword__pb2.PwRequest.SerializeToString,
                response_deserializer=newpassword__pb2.PwReply.FromString,
                )
        self.GetNewNumPass = channel.unary_unary(
                '/newpw.Password/GetNewNumPass',
                request_serializer=newpassword__pb2.PwRequest.SerializeToString,
                response_deserializer=newpassword__pb2.PwReply.FromString,
                )
        self.GetNewLowerPass = channel.unary_unary(
                '/newpw.Password/GetNewLowerPass',
                request_serializer=newpassword__pb2.PwRequest.SerializeToString,
                response_deserializer=newpassword__pb2.PwReply.FromString,
                )
        self.GetNewUpperPass = channel.unary_unary(
                '/newpw.Password/GetNewUpperPass',
                request_serializer=newpassword__pb2.PwRequest.SerializeToString,
                response_deserializer=newpassword__pb2.PwReply.FromString,
                )
        self.GetNewAlphaNumPass = channel.unary_unary(
                '/newpw.Password/GetNewAlphaNumPass',
                request_serializer=newpassword__pb2.PwRequest.SerializeToString,
                response_deserializer=newpassword__pb2.PwReply.FromString,
                )


class PasswordServicer(object):
    """The  service definition.
    """

    def GetNewPass(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNewNumPass(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNewLowerPass(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNewUpperPass(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNewAlphaNumPass(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PasswordServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetNewPass': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNewPass,
                    request_deserializer=newpassword__pb2.PwRequest.FromString,
                    response_serializer=newpassword__pb2.PwReply.SerializeToString,
            ),
            'GetNewNumPass': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNewNumPass,
                    request_deserializer=newpassword__pb2.PwRequest.FromString,
                    response_serializer=newpassword__pb2.PwReply.SerializeToString,
            ),
            'GetNewLowerPass': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNewLowerPass,
                    request_deserializer=newpassword__pb2.PwRequest.FromString,
                    response_serializer=newpassword__pb2.PwReply.SerializeToString,
            ),
            'GetNewUpperPass': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNewUpperPass,
                    request_deserializer=newpassword__pb2.PwRequest.FromString,
                    response_serializer=newpassword__pb2.PwReply.SerializeToString,
            ),
            'GetNewAlphaNumPass': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNewAlphaNumPass,
                    request_deserializer=newpassword__pb2.PwRequest.FromString,
                    response_serializer=newpassword__pb2.PwReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'newpw.Password', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Password(object):
    """The  service definition.
    """

    @staticmethod
    def GetNewPass(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Password/GetNewPass',
            newpassword__pb2.PwRequest.SerializeToString,
            newpassword__pb2.PwReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNewNumPass(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Password/GetNewNumPass',
            newpassword__pb2.PwRequest.SerializeToString,
            newpassword__pb2.PwReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNewLowerPass(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Password/GetNewLowerPass',
            newpassword__pb2.PwRequest.SerializeToString,
            newpassword__pb2.PwReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNewUpperPass(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Password/GetNewUpperPass',
            newpassword__pb2.PwRequest.SerializeToString,
            newpassword__pb2.PwReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNewAlphaNumPass(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/newpw.Password/GetNewAlphaNumPass',
            newpassword__pb2.PwRequest.SerializeToString,
            newpassword__pb2.PwReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
