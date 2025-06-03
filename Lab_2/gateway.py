
# Import required libraries

from flask import Flask, request, jsonify                  # Flask for web framework
from flask_limiter import Limiter                          # Flask-Limiter for rate limiting
from flask_limiter.util import get_remote_address          # Function to get client IP for rate limiting
import jwt                                                 # PyJWT for handling JWT tokens
import requests                                            # For forwarding requests to backend microservices
import os
from dotenv import load_dotenv                             # To load environment variables from .env file

# Load variables from .env (e.g., service URLs and JWT secret key)
load_dotenv()

# Create Flask app
app = Flask(__name__)


# Set up request rate limiting (default: 100 requests/hour per client IP)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100/hour"])


# Get configuration values from environment variables

SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")                      # Secret key to verify JWT
PRODUCT_SERVICE = os.getenv("PRODUCT_SERVICE", "http://localhost:5001") # URL of product microservice
ORDER_SERVICE = os.getenv("ORDER_SERVICE", "http://localhost:5002")     # URL of order microservice
USER_SERVICE = os.getenv("USER_SERVICE", "http://localhost:5003")       # URL of user microservice


# Function to decode and verify JWT token
def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])   # Decode token using secret key
        return decoded                                                   # Return decoded token if valid
    except jwt.InvalidTokenError:
        return None                                                      # Return None if token is invalid


# Middleware to authenticate requests before reaching routes
@app.before_request
def authenticate():
    if request.path.startswith("/public"):
        return                                                           # Skip auth for public routes
    auth = request.headers.get("Authorization", None)
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401                   # Missing or malformed token
    token = auth.split(" ")[1]                                           # Extract token from "Bearer <token>"
    user = verify_jwt(token)
    if not user:
        return jsonify({"error": "Invalid token"}), 403                 # Invalid JWT

    

# Route to proxy requests to Product microservice (rate limit: 50/hour)
@app.route("/product/<path:path>", methods=["GET", "POST"])
@limiter.limit("50/hour")
def proxy_product(path):
    return forward_request(PRODUCT_SERVICE, path)

# Route to proxy requests to Order microservice (rate limit: 30/hour)
@app.route("/order/<path:path>", methods=["GET", "POST"])
@limiter.limit("30/hour")
def proxy_order(path):
    return forward_request(ORDER_SERVICE, path)

# Route to proxy requests to User microservice (rate limit: 20/hour)
@app.route("/user/<path:path>", methods=["GET", "POST"])
@limiter.limit("20/hour")
def proxy_user(path):
    return forward_request(USER_SERVICE, path)

# Helper function to forward the incoming request to the appropriate backend microservice
def forward_request(base_url, path):
    url = f"{base_url}/{path}"                                          # Construct full URL to backend
    headers = {k: v for k, v in request.headers if k.lower() != "host"} # Filter out host header
    data = request.get_json() if request.data else None                 # Include request body if present
    resp = requests.request(method=request.method, url=url, headers=headers, json=data)  # Forward request
    return (resp.text, resp.status_code, resp.headers.items())          # Return response from backend

# Public route to check if the gateway is running
@app.route("/public/health")
def health():
    return "Gateway is up"

# Start the gateway server on port 5000
if __name__ == "__main__":
    app.run(port=5000)
