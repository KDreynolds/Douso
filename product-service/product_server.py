import grpc
from concurrent import futures
import sys
import product_service_pb2
import product_service_pb2_grpc
import time
import logging
import os
from concurrent import futures
import http.server
import socketserver
import threading

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
    
class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Service is running')


def serve_http(port):
    with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
        print(f"Serving health check on port {port}")
        httpd.serve_forever()

        
def serve():
    grpc_port = int(os.environ.get("GRPC_PORT", 50052))  
    http_port = int(os.environ.get("PORT", 8080)) 

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductServicer(), server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    
    print(f"Starting gRPC server on port {grpc_port}")
    server.start()
    
    print(f"Starting HTTP server for health checks on port {http_port}")
    http_thread = threading.Thread(target=serve_http, args=(http_port,))
    http_thread.start()
    
    server.wait_for_termination()

if __name__ == '__main__':
    serve()