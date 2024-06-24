import grpc
import sys
import user_service_pb2
import user_service_pb2_grpc

def get_user_profile(user_id):
    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUserProfile(user_service_pb2.GetUserProfileRequest(user_id=user_id))
        return response

# Example usage
if __name__ == '__main__':
    user_id = 1
    profile = get_user_profile(user_id)
    print(f"User profile for user ID {user_id}: {profile}")