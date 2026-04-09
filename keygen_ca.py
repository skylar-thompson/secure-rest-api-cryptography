'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
KEY GENERATION CA
'''

from Crypto.PublicKey import RSA

# generate RSA key pair
ca_key = RSA.generate(2048)

# save the secret key
with open("secret_ca.key", "wb") as f:
    f.write(ca_key.export_key())

# save the public key
with open("public_ca.key", "wb") as f:
    f.write(ca_key.public_key().export_key())

# output confirmation message upon success
print("CA key pair generated (public_ca.key, secret_ca.key).")
