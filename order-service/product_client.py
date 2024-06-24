import grpc
import sys
import product_service_pb2
import product_service_pb2_grpc

def get_product(product_id):
    with grpc.insecure_channel('product-service:50052') as channel:
        stub = product_service_pb2_grpc.ProductServiceStub(channel)
        response = stub.GetProduct(product_service_pb2.GetProductRequest(product_id=product_id))
        return response

# Example usage
if __name__ == '__main__':
    product_id = 1
    product = get_product(product_id)
    print(f"Product details for product ID {product_id}: {product}")