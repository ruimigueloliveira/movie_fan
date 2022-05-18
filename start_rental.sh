echo "Starting Rental Port 8002"
cd rental/rentals/app
# http://127.0.0.1:8002/rentals/rental/v1/products
python3 -m swagger_server
