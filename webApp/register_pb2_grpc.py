# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import register_pb2 as register__pb2


class RegisterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.registration = channel.unary_unary(
                '/register.Register/registration',
                request_serializer=register__pb2.PwRequest.SerializeToString,
                response_deserializer=register__pb2.PwReply.FromString,
                )


class RegisterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def registration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegisterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'registration': grpc.unary_unary_rpc_method_handler(
                    servicer.registration,
                    request_deserializer=register__pb2.PwRequest.FromString,
                    response_serializer=register__pb2.PwReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'register.Register', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Register(object):
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
        return grpc.experimental.unary_unary(request, target, '/register.Register/registration',
            register__pb2.PwRequest.SerializeToString,
            register__pb2.PwReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
