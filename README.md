# Secure RESTful Communication Suite
CSCE 4050/5050 Project | University of North Texas

## Project Overview
This project implements a secure, multi-layered communication channel between a REST server and client. The architecture evolves from a simple plaintext exchange to a fully secured system utilizing authenticated encryption with associated data (AEAD), asymmetric key transport, and public key infrastructure (PKI) to mitigate man-in-the-middle (MitM) and replay attacks.

## Demo
See the following link for a demo overview and execution of the secure RESTful suite:
https://m.youtube.com/watch?v=B4CwX11r1Ms

## Required Libraries and Installation

### Libraries
   
   * Flask: A micro web framework for building the REST API.

   * PyCryptodome: A self-contained cryptographic library for Python that provides the RSA, AES-GCM, and SHA-256 primitives.

   * Requests: Used by the client to send HTTP GET/POST requests to the server.

### Installation

   1. Create a virtual environment
   ```bash
   python3 -m venv flask-env
   source flask-env/bin/activate  # On Windows: flask-env\Scripts\activate
   ```

   2. Install dependencies
   ```bash
   pip install flask pycryptodome requests
   ```

## File Directory & Purpose
Each file in this repository corresponds to specific requirements defined in the project tasks:

### Core Logic

   * `server.py`: The Flask-based REST server. It handles the /session-key and /weather endpoints, implements the server-side RSA handshake, and decrypts payloads using the dynamic session key.

   * `client.py`: The client that performs the full security handshake, including verifying the server's certificate, encrypting a session key via RSA, and requesting encrypted weather data.

### Security Infrastructure (PKI & Keys)

   * `keygen_ca.py`: Task 4; generates the certificate authority's RSA key pair. This represents a trusted third party.

   * `keygen.py`: Task 3; generates the server's specific RSA key pair used for the asymmetric key exchange.

   * `cert_key.py`: Task 4; this script acts as the CA's signing tool, taking the server's public key and signing it with the CA’s private key to produce pk.cert, incorporating the required Student ID (11681339) into the certificate identity.

### Simulated Attacks and Defense Mechanisms

   * `server_udp.py` & `client_udp.py`: these files implement the Task 2 requirements, demonstrating the transition to AES-GCM authenticated encryption and the implementation of replay attack mitigation using time-drift synchronization before the integration of asymmetric key transport.

   * `server_fake.py`: A malicious server simulation used to validate integrity. It attempts to serve modified data with an intercepted MAC tag to confirm the client detects unauthorized tampering.

   * `server_superfake.py`: A replay attack simulator. It broadcasts a previously captured valid binary response (response.bin) to verify the client's timestamp-based replay protection logic.

## Implemented Security Measures

   * **AES-GCM** (Task 2): Provides authenticated encryption to ensure data confidentiality and integrity.

   * **Replay Protection** (Task 2): Uses timestamp-based validation to ensure captured packets cannot be re-sent.

   * **RSA-2048** (Task 3): Used for secure key transport, allowing the client to securely hand off a session key to the server.

   * **PKI/Digital Certificates** (Task 4): Prevents MitM attacks by forcing the client to verify the server's identity against the CA root before initiating communication.

## Execution Guide
To ensure the chain of trust is established correctly, scripts must be run in this specific order:

### Environment Setup

Generate the cryptographic foundation.

   1. Create the CA:
      ```bash
      python3 keygen_ca.py
      ```

   2. Create the server's RSA identity:
      ```bash
      python3 keygen.py
      ```

   3. Sign the Certificate:
      ```bash
      python3 cert_key.py
      ```

### Deployment

Start the secure environment.

   1. Start the Flask API server:
      ```bash
      python3 server.py
      ```

   2. In a new terminal, run the client:
      ```bash
      python3 client.py
      ```

## Verification
The security of this implementation was audited using Wireshark. Verification confirmed that:

**Identity**: The client successfully rejects any server not presenting a valid pk.cert signed by the CA.

**Confidentiality**: Payloads captured via packet sniffing remain ciphertext.

**Integrity**: Any modification to the encrypted weather_data.bin results in a decryption failure due to the GCM authentication tag.
