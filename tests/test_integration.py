import pytest
import user_service_pb2
import product_service_pb2
import order_service_pb2

def test_create_order(grpc_stubs):
    # Create a user
    user_response = grpc_stubs['user'].RegisterUser(user_service_pb2.RegisterUserRequest(
        username="testuser",
        email="testuser@example.com",
        password="testpassword"
    ))
    assert user_response.user_id > 0

    # Get a product
    product_response = grpc_stubs['product'].GetProduct(product_service_pb2.GetProductRequest(product_id=1))
    assert product_response.product_id == 1

    # Create an order
    order_response = grpc_stubs['order'].CreateOrder(order_service_pb2.CreateOrderRequest(
        user_id=user_response.user_id,
        items=[order_service_pb2.OrderItem(product_id=product_response.product_id, quantity=1)]
    ))
    assert order_response.order_id > 0

    # Check order status
    status_response = grpc_stubs['order'].GetOrderStatus(order_service_pb2.GetOrderStatusRequest(
        order_id=order_response.order_id
    ))
    assert status_response.status == "PENDING"

def test_product_inventory_update(grpc_stubs):
    # Get initial product quantity
    initial_product = grpc_stubs['product'].GetProduct(product_service_pb2.GetProductRequest(product_id=1))
    initial_quantity = initial_product.quantity

    # Create an order
    order_response = grpc_stubs['order'].CreateOrder(order_service_pb2.CreateOrderRequest(
        user_id=1,  # Assuming user 1 exists
        items=[order_service_pb2.OrderItem(product_id=1, quantity=1)]
    ))
    assert order_response.order_id > 0

    # Check updated product quantity
    updated_product = grpc_stubs['product'].GetProduct(product_service_pb2.GetProductRequest(product_id=1))
    assert updated_product.quantity == initial_quantity - 1