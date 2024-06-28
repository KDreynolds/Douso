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
import sentry_sdk
from sentry_sdk import capture_exception, start_span, set_context

sentry_dsn = os.getenv('SENTRY_DSN', "https://ed0e0e87052e01fbe1b36619f3fd4835@o4507498807492608.ingest.us.sentry.io/4507498812276736")
sentry_sdk.init(
    dsn=sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

logging.basicConfig(level=logging.INFO)

class ProductServicer(product_service_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products = {
            1: {"name": "Product 1", "description": "Description 1", "price": 9.99, "quantity": 100},
            2: {"name": "Product 2", "description": "Description 2", "price": 19.99, "quantity": 50},
        }

    def GetProduct(self, request, context):
        with start_span(op="grpc", description="GetProduct"):
            try:
                product_id = request.product_id
                product = self.products.get(product_id)
                if product:
                    set_context("product", product)
                    return product_service_pb2.GetProductResponse(
                        product_id=product_id,
                        name=product['name'],
                        description=product['description'],
                        price=product['price'],
                        quantity=product['quantity']
                    )
                else:
                    error_message = f"Product with ID {product_id} not found"
                    sentry_sdk.capture_message(error_message, level="error")
                    context.abort(grpc.StatusCode.NOT_FOUND, error_message)
            except Exception as e:
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred while getting the product")

    def UpdateInventory(self, request, context):
        with start_span(op="grpc", description="UpdateInventory"):
            try:
                product_id = request.product_id
                quantity_change = request.quantity
                if product_id in self.products:
                    self.products[product_id]['quantity'] += quantity_change
                    new_quantity = self.products[product_id]['quantity']
                    logging.info(f"Updated inventory for Product {product_id}. New quantity: {new_quantity}")
                    set_context("inventory_update", {
                        "product_id": product_id,
                        "quantity_change": quantity_change,
                        "new_quantity": new_quantity
                    })
                    return product_service_pb2.UpdateInventoryResponse(success=True)
                else:
                    error_message = f"Product with ID {product_id} not found"
                    sentry_sdk.capture_message(error_message, level="error")
                    context.abort(grpc.StatusCode.NOT_FOUND, error_message)
            except Exception as e:
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred while updating inventory")

    def SearchProducts(self, request, context):
        with start_span(op="grpc", description="SearchProducts"):
            try:
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
                set_context("search", {
                    "query": query,
                    "results_count": len(matching_products)
                })
                return product_service_pb2.SearchProductsResponse(products=matching_products)
            except Exception as e:
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred while searching products")

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
    try:
        logging.info("Product Service is starting...")
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
    except Exception as e:
        capture_exception(e)
        logging.error(f"An error occurred while starting the server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    serve()