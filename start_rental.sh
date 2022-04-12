echo "Starting Rental"
cd rental/rentals
python3 -mwebbrowser http://127.0.0.1:8080/rentals/rental/v1/products
python3 -m swagger_server
