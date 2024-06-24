import grpc
from concurrent import futures
import sys
import user_service_pb2
import user_service_pb2_grpc

class UserServicer(user_service_pb2_grpc.UserServiceServicer):
    def RegisterUser(self, request, context):
        # Mock the registration logic
        user_id = 1
        return user_service_pb2.RegisterUserResponse(user_id=user_id)

    def LoginUser(self, request, context):
        # Mock the login logic
        access_token = "dummy_token"
        return user_service_pb2.LoginUserResponse(access_token=access_token)

    def GetUserProfile(self, request, context):
        # Mock the user profile retrieval logic
        user_id = request.user_id
        username = "dummy_user"
        email = "dummy@example.com"
        return user_service_pb2.GetUserProfileResponse(user_id=user_id, username=username, email=email)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')  
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()