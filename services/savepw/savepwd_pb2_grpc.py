# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import savepwd_pb2 as savepwd__pb2


class SaverStub(object):
    """The  service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SavePw = channel.unary_unary(
                '/savepw.Saver/SavePw',
                request_serializer=savepwd__pb2.SaveRequest.SerializeToString,
                response_deserializer=savepwd__pb2.SaveReply.FromString,
                )


class SaverServicer(object):
    """The  service definition.
    """

    def SavePw(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SaverServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SavePw': grpc.unary_unary_rpc_method_handler(
                    servicer.SavePw,
                    request_deserializer=savepwd__pb2.SaveRequest.FromString,
                    response_serializer=savepwd__pb2.SaveReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'savepw.Saver', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Saver(object):
    """The  service definition.
    """

    @staticmethod
    def SavePw(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/savepw.Saver/SavePw',
            savepwd__pb2.SaveRequest.SerializeToString,
            savepwd__pb2.SaveReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
