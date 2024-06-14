import grpc
from concurrent import futures
import sys
import product_service_pb2
import product_service_pb2_grpc

class ProductServicer(product_service_pb2_grpc.ProductServiceServicer):
    def GetProduct(self, request, context):
        # Mock the product retrieval logic
        product_id = request.product_id
        name = "dummy_product"
        description = "This is a dummy product"
        price = 9.99
        quantity = 100
        return product_service_pb2.GetProductResponse(product_id=product_id, name=name, description=description, price=price, quantity=quantity)

    def SearchProducts(self, request, context):
        # Mock the product search logic
        query = request.query
        products = [
            product_service_pb2.GetProductResponse(product_id=1, name="Product 1", description="Description 1", price=9.99, quantity=100),
            product_service_pb2.GetProductResponse(product_id=2, name="Product 2", description="Description 2", price=19.99, quantity=50)
        ]
        return product_service_pb2.SearchProductsResponse(products=products)

    def UpdateInventory(self, request, context):
        # Mock the inventory update logic
        product_id = request.product_id
        quantity = request.quantity
        success = True
        return product_service_pb2.UpdateInventoryResponse(success=success)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()