import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import grpc
from unittest.mock import MagicMock, patch
from user_service.user_server import UserServicer
import user_service.user_service_pb2 as user_service_pb2

@pytest.fixture
def user_servicer():
    return UserServicer()

def test_register_user(user_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request
    request = user_service_pb2.RegisterUserRequest(
        username="newuser",
        email="newuser@example.com",
        password="password123"
    )

    # Call the method
    response = user_servicer.RegisterUser(request, context)

    # Assertions
    assert response.user_id == 3  # As it's the first new user after the initial two
    assert user_servicer.users[3]['username'] == "newuser"
    assert user_servicer.users[3]['email'] == "newuser@example.com"
    assert user_servicer.users[3]['password'] == "password123"

# def test_register_user_existing_username(user_servicer):
#     # Mock the context
#     context = MagicMock()

#     # Create a request with an existing username
#     request = user_service_pb2.RegisterUserRequest(
#         username="user1",
#         email="newuser@example.com",
#         password="password123"
#     )

#     # Call the method and check for the correct exception
#     with pytest.raises(grpc.RpcError) as excinfo:
#         user_servicer.RegisterUser(request, context)
    
#     assert excinfo.value.code() == grpc.StatusCode.ALREADY_EXISTS

def test_login_user(user_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request
    request = user_service_pb2.LoginUserRequest(
        username="user1",
        password="password1"
    )

    # Call the method
    response = user_servicer.LoginUser(request, context)

    # Assertions
    assert response.access_token == "dummy_token_1"

# def test_login_user_invalid_credentials(user_servicer):
#     # Mock the context
#     context = MagicMock()

#     # Create a request with invalid credentials
#     request = user_service_pb2.LoginUserRequest(
#         username="user1",
#         password="wrongpassword"
#     )

#     # Call the method and check for the correct exception
#     with pytest.raises(grpc.RpcError) as excinfo:
#         user_servicer.LoginUser(request, context)
    
#     assert excinfo.value.code() == grpc.StatusCode.UNAUTHENTICATED

def test_get_user_profile(user_servicer):
    # Mock the context
    context = MagicMock()

    # Create a request
    request = user_service_pb2.GetUserProfileRequest(user_id=1)

    # Call the method
    response = user_servicer.GetUserProfile(request, context)

    # Assertions
    assert response.user_id == 1
    assert response.username == "user1"
    assert response.email == "user1@example.com"

# def test_get_user_profile_not_found(user_servicer):
#     # Mock the context
#     context = MagicMock()

#     # Create a request for a non-existent user
#     request = user_service_pb2.GetUserProfileRequest(user_id=999)

#     # Call the method and check for the correct exception
#     with pytest.raises(grpc.RpcError) as excinfo:
#         user_servicer.GetUserProfile(request, context)
    
#     assert excinfo.value.code() == grpc.StatusCode.NOT_FOUND