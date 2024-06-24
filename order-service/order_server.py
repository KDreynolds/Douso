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

logging.basicConfig(level=logging.INFO)

class OrderServicer(order_service_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}
        self.order_id_counter = 1

    def CreateOrder(self, request, context):
        order_id = self.order_id_counter
        self.order_id_counter += 1
        self.orders[order_id] = {"user_id": request.user_id, "items": request.items, "status": "PENDING"}
        logging.info(f"Order {order_id} created for User {request.user_id}. Items: {[item.product_id for item in request.items]}")
    
        # Update inventory for each item in the order
        with grpc.insecure_channel('product-service:50052') as channel:
            product_stub = product_service_pb2_grpc.ProductServiceStub(channel)
            for item in request.items:
                product_stub.UpdateInventory(product_service_pb2.UpdateInventoryRequest(
                    product_id=item.product_id, 
                    quantity=-item.quantity
             ))
    
        return order_service_pb2.CreateOrderResponse(order_id=order_id)

    def GetOrderStatus(self, request, context):
        order_id = request.order_id
        order = self.orders.get(order_id)
        if order:
            return order_service_pb2.GetOrderStatusResponse(order_id=order_id, status=order['status'])
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Order with ID {order_id} not found")

    def CancelOrder(self, request, context):
        order_id = request.order_id
        if order_id in self.orders:
            self.orders[order_id]['status'] = 'CANCELLED'
            return order_service_pb2.CancelOrderResponse(success=True)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Order with ID {order_id} not found")

def create_dummy_order():
    with grpc.insecure_channel('user-service:50051') as user_channel, \
         grpc.insecure_channel('product-service:50052') as product_channel:
        user_stub = user_service_pb2_grpc.UserServiceStub(user_channel)
        product_stub = product_service_pb2_grpc.ProductServiceStub(product_channel)

        user_id = random.randint(1, 2)
        product_id = random.randint(1, 2)

        try:
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
            if status_code == grpc.StatusCode.UNIMPLEMENTED:
                print(f"Method not implemented: {e.details()}")
            elif status_code == grpc.StatusCode.UNAVAILABLE:
                print(f"Service unavailable: {e.details()}")
            else:
                print(f"An error occurred: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
    port = int(os.environ.get("PORT", 50053))
    server.add_insecure_port('0.0.0.0:50053')
    server.start()
    print("Order Service started on port 50053")

    while True:
        time.sleep(5)  # Wait for 5 seconds
        create_dummy_order()

if __name__ == '__main__':
    serve()