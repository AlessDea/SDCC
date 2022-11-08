# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos.sharedpw_pb2 as sharedpw__pb2


class SharedStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.passwordRequest = channel.unary_unary(
                '/sharedpw.Shared/passwordRequest',
                request_serializer=sharedpw__pb2.SharedPasswordRequest.SerializeToString,
                response_deserializer=sharedpw__pb2.SharedPasswordReply.FromString,
                )
        self.checkPassword = channel.unary_unary(
                '/sharedpw.Shared/checkPassword',
                request_serializer=sharedpw__pb2.CheckSharedPasswordRequest.SerializeToString,
                response_deserializer=sharedpw__pb2.CheckSharedPasswordReply.FromString,
                )


class SharedServicer(object):
    """Missing associated documentation comment in .proto file."""

    def passwordRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkPassword(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SharedServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'passwordRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.passwordRequest,
                    request_deserializer=sharedpw__pb2.SharedPasswordRequest.FromString,
                    response_serializer=sharedpw__pb2.SharedPasswordReply.SerializeToString,
            ),
            'checkPassword': grpc.unary_unary_rpc_method_handler(
                    servicer.checkPassword,
                    request_deserializer=sharedpw__pb2.CheckSharedPasswordRequest.FromString,
                    response_serializer=sharedpw__pb2.CheckSharedPasswordReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sharedpw.Shared', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Shared(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def passwordRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sharedpw.Shared/passwordRequest',
            sharedpw__pb2.SharedPasswordRequest.SerializeToString,
            sharedpw__pb2.SharedPasswordReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkPassword(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sharedpw.Shared/checkPassword',
            sharedpw__pb2.CheckSharedPasswordRequest.SerializeToString,
            sharedpw__pb2.CheckSharedPasswordReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
