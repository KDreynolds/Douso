import grpc
import user_service_pb2
import user_service_pb2_grpc

def get_user_profile(user_id):
    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUserProfile(user_service_pb2.GetUserProfileRequest(user_id=user_id))
        return response

def register_user(username, email, password):
    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.RegisterUser(user_service_pb2.RegisterUserRequest(username=username, email=email, password=password))
        return response

def login_user(username, password):
    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.LoginUser(user_service_pb2.LoginUserRequest(username=username, password=password))
        return response

if __name__ == '__main__':
    # Example usage
    new_user = register_user("newuser", "newuser@example.com", "password123")
    print(f"Registered new user with ID: {new_user.user_id}")

    login_response = login_user("newuser", "password123")
    print(f"Login token: {login_response.access_token}")

    user_profile = get_user_profile(new_user.user_id)
    print(f"User profile: {user_profile}")