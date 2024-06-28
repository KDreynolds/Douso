import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import grpc
from unittest.mock import MagicMock, patch
from product_service.product_server import ProductServicer
import product_service.product_service_pb2 as product_service_pb2

@pytest.fixture
def product_servicer():
    return ProductServicer()

def test_get_product(product_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request for an existing product
    request = product_service_pb2.GetProductRequest(product_id=1)

    # Call the method
    response = product_servicer.GetProduct(request, context)

    # Assertions
    assert response.product_id == 1
    assert response.name == "Product 1"
    assert response.description == "Description 1"
    assert response.price == 9.99
    assert response.quantity == 100

def test_get_product_not_found(product_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request for a non-existent product
    request = product_service_pb2.GetProductRequest(product_id=999)

    # Call the method and check for the correct exception
    with pytest.raises(grpc.RpcError) as excinfo:
        product_servicer.GetProduct(request, context)
    
    assert excinfo.value.code() == grpc.StatusCode.NOT_FOUND

def test_update_inventory(product_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request
    request = product_service_pb2.UpdateInventoryRequest(product_id=1, quantity=-10)

    # Call the method
    response = product_servicer.UpdateInventory(request, context)

    # Assertions
    assert response.success == True
    assert product_servicer.products[1]['quantity'] == 90

def test_update_inventory_not_found(product_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request for a non-existent product
    request = product_service_pb2.UpdateInventoryRequest(product_id=999, quantity=-10)

    # Call the method and check for the correct exception
    with pytest.raises(grpc.RpcError) as excinfo:
        product_servicer.UpdateInventory(request, context)
    
    assert excinfo.value.code() == grpc.StatusCode.NOT_FOUND

def test_search_products(product_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request
    request = product_service_pb2.SearchProductsRequest(query="Product")

    # Call the method
    response = product_servicer.SearchProducts(request, context)

    # Assertions
    assert len(response.products) == 2
    assert response.products[0].name == "Product 1"
    assert response.products[1].name == "Product 2"

def test_search_products_no_results(product_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request with a query that shouldn't match any products
    request = product_service_pb2.SearchProductsRequest(query="NonexistentProduct")

    # Call the method
    response = product_servicer.SearchProducts(request, context)

    # Assertions
    assert len(response.products) == 0