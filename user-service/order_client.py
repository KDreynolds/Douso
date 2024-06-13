import grpc
import sys
import order_service_pb2
import order_service_pb2_grpc

def get_order_status(order_id):
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = order_service_pb2_grpc.OrderServiceStub(channel)
        response = stub.GetOrderStatus(order_service_pb2.GetOrderStatusRequest(order_id=order_id))
        return response.status

# Example usage
if __name__ == '__main__':
    order_id = 1
    status = get_order_status(order_id)
    print(f"Order status for order ID {order_id}: {status}")