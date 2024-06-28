import grpc
from concurrent import futures
import sys
import user_service_pb2
import user_service_pb2_grpc
import time
import logging
import os
from concurrent import futures
import http.server
import socketserver
import threading
import sentry_sdk
from sentry_sdk import capture_exception, start_span

sentry_sdk.init(
    dsn="https://ed0e0e87052e01fbe1b36619f3fd4835@o4507498807492608.ingest.us.sentry.io/4507498812276736",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


logging.basicConfig(level=logging.INFO)


class UserServicer(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {
            1: {"username": "user1", "email": "user1@example.com", "password": "password1"},
            2: {"username": "user2", "email": "user2@example.com", "password": "password2"},
        }
        self.next_user_id = 3

    def RegisterUser(self, request, context):
        with start_span(op="grpc", description="RegisterUser"):
            try:
                for user in self.users.values():
                    if user['username'] == request.username or user['email'] == request.email:
                        error_message = "Username or email already exists"
                        sentry_sdk.capture_message(error_message, level="error")
                        context.abort(grpc.StatusCode.ALREADY_EXISTS, error_message)
            
                user_id = self.next_user_id
                self.next_user_id += 1
                self.users[user_id] = {
                    "username": request.username,
                    "email": request.email,
                    "password": request.password  # In a real application, you should hash the password
                }
                return user_service_pb2.RegisterUserResponse(user_id=user_id)
            except Exception as e:
                capture_exception(e)
                logging.error(f"An error occurred: {str(e)}")
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred")

    def LoginUser(self, request, context):
        with start_span(op="grpc", description="LoginUser"):
            try:
                for user_id, user in self.users.items():
                    if user['username'] == request.username and user['password'] == request.password:
                        return user_service_pb2.LoginUserResponse(access_token=f"dummy_token_{user_id}")
                
                error_message = "Invalid username or password"
                sentry_sdk.capture_message(error_message, level="error")
                context.abort(grpc.StatusCode.UNAUTHENTICATED, error_message)
            except Exception as e:
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred")

    def GetUserProfile(self, request, context):
        with start_span(op="grpc", description="GetUserProfile"):
            try:
                user_id = request.user_id
                user = self.users.get(user_id)
                logging.info(f"Profile requested for User {user_id}")
                if user:
                    return user_service_pb2.GetUserProfileResponse(user_id=user_id, username=user['username'], email=user['email'])
                else:
                    error_message = f"User with ID {user_id} not found"
                    logging.error(error_message)
                    sentry_sdk.capture_message(error_message, level="error")
                    context.abort(grpc.StatusCode.NOT_FOUND, error_message)
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                capture_exception(e)
                context.abort(grpc.StatusCode.INTERNAL, "An internal error occurred")

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Service is running')

def serve_http(port):
    with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
        print(f"Serving health check on port {port}")
        httpd.serve_forever()

def serve():
    try:
        logging.info("User Service is starting...")
        grpc_port = int(os.environ.get("GRPC_PORT", 50051)) 
        http_port = int(os.environ.get("PORT", 8080))  

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
        server.add_insecure_port(f'[::]:{grpc_port}')
        
        print(f"Starting gRPC server on port {grpc_port}")
        server.start()
        
        print(f"Starting HTTP server for health checks on port {http_port}")
        http_thread = threading.Thread(target=serve_http, args=(http_port,))
        http_thread.start()
        
        server.wait_for_termination()
    except Exception as e:
        capture_exception(e)
        logging.error(f"An error occurred while starting the server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    serve()