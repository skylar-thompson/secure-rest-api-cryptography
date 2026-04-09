'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
KEY CERTIFICATION
'''

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# load server's public key to be certified
with open("public.key", "rb") as f:
    server_pub_key = RSA.import_key(f.read())
    server_pub_hex = server_pub_key.export_key().hex()

# load CA's secret key to sign the message
with open("secret_ca.key", "rb") as f:
    ca_secret_key = RSA.import_key(f.read())

# create the message using Skylar's student ID (11681339)
message = f"This public key: {server_pub_hex} belongs to (ID: 11681339)".encode('utf-8')

# sign the message
h = SHA256.new(message)
signature = pkcs1_15.new(ca_secret_key).sign(h)

# save the message + signature to pk.cert
with open("pk.cert", "wb") as f:
    # We save both so the client can verify the signature against the message
    f.write(message + b"||SIGNATURE||" + signature)

# output message upon successful completion
print("Certificate 'pk.cert' generated and signed by CA.")
