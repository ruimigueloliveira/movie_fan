#!/usr/bin/env python3

import connexion

from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Rental API'}, pythonic_params=True)
    app.run(port=8080)


@app.route('/products/12', methods=['POST'])
def products_id_post(id):
    return "Hello"

if __name__ == '__main__':
    main()
