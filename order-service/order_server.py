import grpc
from concurrent import futures
import sys
import order_service_pb2
import order_service_pb2_grpc

class OrderServicer(order_service_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        # Mock the order creation logic
        user_id = request.user_id
        items = request.items
        order_id = 1
        return order_service_pb2.CreateOrderResponse(order_id=order_id)

    def GetOrderStatus(self, request, context):
        # Mock the order status retrieval logic
        order_id = request.order_id
        status = "PENDING"
        return order_service_pb2.GetOrderStatusResponse(order_id=order_id, status=status)

    def CancelOrder(self, request, context):
        # Mock the order cancellation logic
        order_id = request.order_id
        success = True
        return order_service_pb2.CancelOrderResponse(success=success)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()