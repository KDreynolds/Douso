import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import grpc
from unittest.mock import MagicMock, patch
from order_service.order_server import OrderServicer
import order_service.order_service_pb2 as order_service_pb2
import product_service.product_service_pb2 as product_service_pb2


@pytest.fixture
def order_servicer():
    return OrderServicer()

def test_create_order(order_servicer):
    # Mock the context and product stub
    context = MagicMock()
    with patch('order_service.order_server.product_service_pb2_grpc.ProductServiceStub') as MockProductStub:
        mock_product_stub = MockProductStub.return_value
        mock_product_stub.UpdateInventory.return_value = product_service_pb2.UpdateInventoryResponse(success=True)

        # Create a request
        request = order_service_pb2.CreateOrderRequest(
            user_id=1,
            items=[order_service_pb2.OrderItem(product_id=1, quantity=2)]
        )

        # Call the method
        response = order_servicer.CreateOrder(request, context)

        # Assertions
        assert response.order_id == 1
        assert len(order_servicer.orders) == 1
        assert order_servicer.orders[1]['status'] == 'PENDING'
        mock_product_stub.UpdateInventory.assert_called_once()

def test_get_order_status(order_servicer):
    # Create an order
    order_servicer.orders[1] = {"user_id": 1, "items": [], "status": "PENDING"}

    # Mock the context
    context = MagicMock()

    # Create a request
    request = order_service_pb2.GetOrderStatusRequest(order_id=1)

    # Call the method
    response = order_servicer.GetOrderStatus(request, context)

    # Assertions
    assert response.order_id == 1
    assert response.status == "PENDING"

# def test_get_order_status_not_found(order_servicer):
#     # Mock the context
#     context = MagicMock()

#     # Create a request for a non-existent order
#     request = order_service_pb2.GetOrderStatusRequest(order_id=999)

#     # Call the method and check for the correct exception
#     with pytest.raises(grpc.RpcError) as excinfo:
#         order_servicer.GetOrderStatus(request, context)
    
#     assert excinfo.value.code() == grpc.StatusCode.NOT_FOUND
#     context.abort.assert_called_once_with(grpc.StatusCode.NOT_FOUND, "Order with ID 999 not found")

def test_cancel_order(order_servicer):
    # Create an order
    order_servicer.orders[1] = {"user_id": 1, "items": [], "status": "PENDING"}

    # Mock the context
    context = MagicMock()

    # Create a request
    request = order_service_pb2.CancelOrderRequest(order_id=1)

    # Call the method
    response = order_servicer.CancelOrder(request, context)

    # Assertions
    assert response.success == True
    assert order_servicer.orders[1]['status'] == 'CANCELLED'

# def test_cancel_order_not_found(order_servicer):
#     # Mock the context
#     context = MagicMock()

#     # Create a request for a non-existent order
#     request = order_service_pb2.CancelOrderRequest(order_id=999)

#     # Call the method and check for the correct exception
#     with pytest.raises(grpc.RpcError) as excinfo:
#         order_servicer.CancelOrder(request, context)
    
#     assert excinfo.value.code() == grpc.StatusCode.NOT_FOUND
#     context.abort.assert_called_once_with(grpc.StatusCode.NOT_FOUND, "Order with ID 999 not found")