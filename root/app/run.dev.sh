#!/bin/sh

# Use the server's self-signed public key.
export SSL_CERT_FILE=/etc/tt/certs/tt-fullchain.pem

# Run the Python client.
python3 main.py