'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
KEY GENERATION
'''

from Crypto.PublicKey import RSA

#generating a key
key = RSA.generate(2048)

#extracting private key
secret_key = key.export_key()
#extracting public key
public_key = key.public_key().export_key()

with open("secret.key", "wb") as f:
    f.write(secret_key)
with open("public.key", "wb") as f:
    f.write(public_key)






