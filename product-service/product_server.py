import grpc
from concurrent import futures
import sys
import product_service_pb2
import product_service_pb2_grpc
import time
import logging
import os

logging.basicConfig(level=logging.INFO)


class ProductServicer(product_service_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products = {
            1: {"name": "Product 1", "description": "Description 1", "price": 9.99, "quantity": 100},
            2: {"name": "Product 2", "description": "Description 2", "price": 19.99, "quantity": 50},
        }

    def GetProduct(self, request, context):
        product_id = request.product_id
        product = self.products.get(product_id)
        if product:
            return product_service_pb2.GetProductResponse(
                product_id=product_id,
                name=product['name'],
                description=product['description'],
                price=product['price'],
                quantity=product['quantity']
            )
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Product with ID {product_id} not found")

    def UpdateInventory(self, request, context):
        product_id = request.product_id
        quantity_change = request.quantity
        logging.info(f"Updated inventory for Product {product_id}. New quantity: {self.products[product_id]['quantity']}")
        if product_id in self.products:
            self.products[product_id]['quantity'] += quantity_change
            return product_service_pb2.UpdateInventoryResponse(success=True)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Product with ID {product_id} not found")

    def SearchProducts(self, request, context):
        query = request.query.lower()
        matching_products = [
            product_service_pb2.GetProductResponse(
                product_id=product_id,
                name=product['name'],
                description=product['description'],
                price=product['price'],
                quantity=product['quantity']
            )
            for product_id, product in self.products.items()
            if query in product['name'].lower() or query in product['description'].lower()
        ]
        return product_service_pb2.SearchProductsResponse(products=matching_products)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductServicer(), server)
    port = int(os.environ.get("PORT", 50052))
    server.add_insecure_port('0.0.0.0:50052')
    server.start()
    print("Product Service started on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()