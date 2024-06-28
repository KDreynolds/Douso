import grpc
import product_service_pb2
import product_service_pb2_grpc

def update_inventory(product_id, quantity):
    with grpc.insecure_channel('product-service:50052') as channel:
        stub = product_service_pb2_grpc.ProductServiceStub(channel)
        response = stub.UpdateInventory(product_service_pb2.UpdateInventoryRequest(product_id=product_id, quantity=quantity))
        return response.success

# Example usage
if __name__ == '__main__':
    product_id = 1
    quantity = -10
    success = update_inventory(product_id, quantity)
    print(f"Inventory update for product ID {product_id}: {'Success' if success else 'Failure'}")