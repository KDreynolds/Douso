import grpc
import sys
import order_service_pb2
import order_service_pb2_grpc

def update_inventory(product_id, quantity):
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = order_service_pb2_grpc.OrderServiceStub(channel)
        response = stub.UpdateInventory(order_service_pb2.UpdateInventoryRequest(product_id=product_id, quantity=quantity))
        return response.success

# Example usage
if __name__ == '__main__':
    product_id = 1
    quantity = -10
    success = update_inventory(product_id, quantity)
    print(f"Inventory update for product ID {product_id}: {'Success' if success else 'Failure'}")