import grpc
from concurrent import futures
import sys
import order_service_pb2
import order_service_pb2_grpc
import user_service_pb2
import user_service_pb2_grpc
import product_service_pb2
import product_service_pb2_grpc
import time
import random
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

class OrderServicer(order_service_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}
        self.order_id_counter = 1

    def CreateOrder(self, request, context):
        with start_span(op="grpc", description="CreateOrder"):
            try:
                order_id = self.order_id_counter
                self.order_id_counter += 1
                self.orders[order_id] = {"user_id": request.user_id, "items": request.items, "status": "PENDING"}
                logging.info(f"Order {order_id} created for User {request.user_id}. Items: {[item.product_id for item in request.items]}")
                
                set_context("order", {
                    "order_id": order_id,
                    "user_id": request.user_id,
                    "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in request.items]
                })

                # Update inventory for each item in the order
                with grpc.insecure_channel('product-service:50052') as channel:
                    product_stub = product_service_pb2_grpc.ProductServiceStub(channel)
                    for item in request.items:
                        product_stub.UpdateInventory(product_service_pb2.UpdateInventoryRequest(
                            product_id=item.product_id, 
                            quantity=-item.quantity
                        ))

                return order_service_pb2.CreateOrderResponse(order_id=order_id)
            except Exception as e:
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred while creating the order")

    def GetOrderStatus(self, request, context):
        with start_span(op="grpc", description="GetOrderStatus"):
            try:
                order_id = request.order_id
                order = self.orders.get(order_id)
                if order:
                    return order_service_pb2.GetOrderStatusResponse(order_id=order_id, status=order['status'])
                else:
                    error_message = f"Order with ID {order_id} not found"
                    sentry_sdk.capture_message(error_message, level="error")
                    context.abort(grpc.StatusCode.NOT_FOUND, error_message)
            except Exception as e:
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred while getting order status")

    def CancelOrder(self, request, context):
        with start_span(op="grpc", description="CancelOrder"):
            try:
                order_id = request.order_id
                if order_id in self.orders:
                    self.orders[order_id]['status'] = 'CANCELLED'
                    return order_service_pb2.CancelOrderResponse(success=True)
                else:
                    error_message = f"Order with ID {order_id} not found"
                    sentry_sdk.capture_message(error_message, level="error")
                    context.abort(grpc.StatusCode.NOT_FOUND, error_message)
            except Exception as e:
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred while cancelling the order")

def create_dummy_order():
    with start_span(op="dummy_order", description="Create Dummy Order"):
        try:
            with grpc.insecure_channel('user-service:50051') as user_channel, \
                 grpc.insecure_channel('product-service:50052') as product_channel:
                user_stub = user_service_pb2_grpc.UserServiceStub(user_channel)
                product_stub = product_service_pb2_grpc.ProductServiceStub(product_channel)

                user_id = random.randint(1, 2)
                product_id = random.randint(1, 2)

                user = user_stub.GetUserProfile(user_service_pb2.GetUserProfileRequest(user_id=user_id))
                product = product_stub.GetProduct(product_service_pb2.GetProductRequest(product_id=product_id))

                logging.info(f"Creating order for User: {user.username}, Product: {product.name}")

                order_stub = order_service_pb2_grpc.OrderServiceStub(grpc.insecure_channel('order-service:50053'))
                order = order_stub.CreateOrder(order_service_pb2.CreateOrderRequest(
                    user_id=user_id,
                    items=[order_service_pb2.OrderItem(product_id=product_id, quantity=1)]
                ))

                logging.info(f"Order created with ID: {order.order_id}")

        except grpc.RpcError as e:
            status_code = e.code()
            error_message = f"gRPC error: {status_code}, {e.details()}"
            sentry_sdk.capture_message(error_message, level="error")
            logging.error(error_message)
        except Exception as e:
            capture_exception(e)
            logging.error(f"An error occurred: {str(e)}")

def create_dummy_orders():
    while True:
        create_dummy_order()
        time.sleep(10)

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
        logging.info("Order Service is starting...")
        grpc_port = int(os.environ.get("GRPC_PORT", 50053))  
        http_port = int(os.environ.get("PORT", 8080))  

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        order_service_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
        server.add_insecure_port(f'[::]:{grpc_port}')
        
        print(f"Starting gRPC server on port {grpc_port}")
        server.start()
        
        print(f"Starting HTTP server for health checks on port {http_port}")
        http_thread = threading.Thread(target=serve_http, args=(http_port,))
        http_thread.start()

        dummy_order_thread = threading.Thread(target=create_dummy_orders)
        dummy_order_thread.start()
        
        server.wait_for_termination()
    except Exception as e:
        capture_exception(e)
        logging.error(f"An error occurred while starting the server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    serve()