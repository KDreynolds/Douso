# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import product_service_pb2 as product__service__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in product_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ProductServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProduct = channel.unary_unary(
                '/product_service.ProductService/GetProduct',
                request_serializer=product__service__pb2.GetProductRequest.SerializeToString,
                response_deserializer=product__service__pb2.GetProductResponse.FromString,
                _registered_method=True)
        self.SearchProducts = channel.unary_unary(
                '/product_service.ProductService/SearchProducts',
                request_serializer=product__service__pb2.SearchProductsRequest.SerializeToString,
                response_deserializer=product__service__pb2.SearchProductsResponse.FromString,
                _registered_method=True)
        self.UpdateInventory = channel.unary_unary(
                '/product_service.ProductService/UpdateInventory',
                request_serializer=product__service__pb2.UpdateInventoryRequest.SerializeToString,
                response_deserializer=product__service__pb2.UpdateInventoryResponse.FromString,
                _registered_method=True)


class ProductServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchProducts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateInventory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProductServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProduct,
                    request_deserializer=product__service__pb2.GetProductRequest.FromString,
                    response_serializer=product__service__pb2.GetProductResponse.SerializeToString,
            ),
            'SearchProducts': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchProducts,
                    request_deserializer=product__service__pb2.SearchProductsRequest.FromString,
                    response_serializer=product__service__pb2.SearchProductsResponse.SerializeToString,
            ),
            'UpdateInventory': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateInventory,
                    request_deserializer=product__service__pb2.UpdateInventoryRequest.FromString,
                    response_serializer=product__service__pb2.UpdateInventoryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'product_service.ProductService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('product_service.ProductService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ProductService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/product_service.ProductService/GetProduct',
            product__service__pb2.GetProductRequest.SerializeToString,
            product__service__pb2.GetProductResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SearchProducts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/product_service.ProductService/SearchProducts',
            product__service__pb2.SearchProductsRequest.SerializeToString,
            product__service__pb2.SearchProductsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateInventory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/product_service.ProductService/UpdateInventory',
            product__service__pb2.UpdateInventoryRequest.SerializeToString,
            product__service__pb2.UpdateInventoryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
