import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import grpc
import time
import user_service.user_service_pb2_grpc as user_service_pb2_grpc
import product_service.product_service_pb2_grpc as product_service_pb2_grpc
import order_service.order_service_pb2_grpc as order_service_pb2_grpc
from order_service.order_server import OrderServicer
from product_service.product_server import ProductServicer
from user_service.user_server import UserServicer

@pytest.fixture
def user_servicer():
    return UserServicer()

@pytest.fixture
def product_servicer():
    return ProductServicer()

@pytest.fixture
def order_servicer():
    return OrderServicer()

def wait_for_service(service_name, port, max_attempts=10, delay=2):
    channel = grpc.insecure_channel(f'{service_name}:{port}')
    for attempt in range(max_attempts):
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
            return
        except grpc.FutureTimeoutError:
            if attempt == max_attempts - 1:
                pytest.fail(f"Service {service_name} on port {port} is not available")
            time.sleep(delay)

@pytest.fixture(scope="session")
def grpc_channels():
    wait_for_service('user-service', 50051)
    wait_for_service('product-service', 50052)
    wait_for_service('order-service', 50053)

    user_channel = grpc.insecure_channel('user-service:50051')
    product_channel = grpc.insecure_channel('product-service:50052')
    order_channel = grpc.insecure_channel('order-service:50053')

    yield {
        'user': user_channel,
        'product': product_channel,
        'order': order_channel
    }

    user_channel.close()
    product_channel.close()
    order_channel.close()

@pytest.fixture(scope="session")
def grpc_stubs(grpc_channels):
    return {
        'user': user_service_pb2_grpc.UserServiceStub(grpc_channels['user']),
        'product': product_service_pb2_grpc.ProductServiceStub(grpc_channels['product']),
        'order': order_service_pb2_grpc.OrderServiceStub(grpc_channels['order'])
    }