# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos.listing_pb2 as listing__pb2


class ListingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.doList = channel.unary_unary(
                '/listing.Listing/doList',
                request_serializer=listing__pb2.ListRequest.SerializeToString,
                response_deserializer=listing__pb2.ListReply.FromString,
                )


class ListingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def doList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ListingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'doList': grpc.unary_unary_rpc_method_handler(
                    servicer.doList,
                    request_deserializer=listing__pb2.ListRequest.FromString,
                    response_serializer=listing__pb2.ListReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'listing.Listing', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Listing(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def doList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/listing.Listing/doList',
            listing__pb2.ListRequest.SerializeToString,
            listing__pb2.ListReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
