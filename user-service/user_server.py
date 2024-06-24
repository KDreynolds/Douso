import grpc
from concurrent import futures
import sys
import user_service_pb2
import user_service_pb2_grpc
import time
import logging
import os

logging.basicConfig(level=logging.INFO)


class UserServicer(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {
            1: {"username": "user1", "email": "user1@example.com", "password": "password1"},
            2: {"username": "user2", "email": "user2@example.com", "password": "password2"},
        }
        self.next_user_id = 3

    def RegisterUser(self, request, context):
        for user in self.users.values():
            if user['username'] == request.username or user['email'] == request.email:
                context.abort(grpc.StatusCode.ALREADY_EXISTS, "Username or email already exists")
        
        user_id = self.next_user_id
        self.next_user_id += 1
        self.users[user_id] = {
            "username": request.username,
            "email": request.email,
            "password": request.password  # In a real application, you should hash the password
        }
        return user_service_pb2.RegisterUserResponse(user_id=user_id)

    def LoginUser(self, request, context):
        for user_id, user in self.users.items():
            if user['username'] == request.username and user['password'] == request.password:
                # In a real application, you should use a proper authentication system
                return user_service_pb2.LoginUserResponse(access_token=f"dummy_token_{user_id}")
        
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid username or password")

    def GetUserProfile(self, request, context):
        user_id = request.user_id
        user = self.users.get(user_id)
        logging.info(f"Profile requested for User {user_id}")
        if user:
            return user_service_pb2.GetUserProfileResponse(user_id=user_id, username=user['username'], email=user['email'])
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, f"User with ID {user_id} not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    port = int(os.environ.get("PORT", 50051))
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("User Service started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()