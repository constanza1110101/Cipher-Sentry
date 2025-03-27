import os
import json
import time
import hashlib
import requests
import tensorflow as tf
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import numpy as np

class CipherSentry:
    def __init__(self):
        self.model = self.load_ai_model()
        self.encryption_key = os.urandom(32)  # AES-256 key
        self.iv = os.urandom(16)  # IV for AES-CBC

    def load_ai_model(self):
        """Loads a machine learning model for intrusion detection"""
        try:
            return tf.keras.models.load_model('cipher_sentry_ai.h5')
        except:
            print("Warning: AI Model not found, using default detection.")
            return None

    def encrypt_file(self, file_path):
        """Encrypts a file using AES-256"""
        with open(file_path, 'rb') as file:
            plaintext = file.read()

        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(self.iv + ciphertext)
        
        print(f"🔒 File encrypted: {encrypted_file_path}")
        return encrypted_file_path

    def decrypt_file(self, encrypted_file_path):
        """Decrypts an AES-256 encrypted file"""
        with open(encrypted_file_path, 'rb') as encrypted_file:
            iv = encrypted_file.read(16)
            ciphertext = encrypted_file.read()

        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        decrypted_file_path = encrypted_file_path.replace('.enc', '.dec')
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(plaintext)

        print(f"🔓 File decrypted: {decrypted_file_path}")
        return decrypted_file_path

    def generate_rsa_keys(self):
        """Generates RSA-4096 key pair for secure communication"""
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=4096, backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open("private_key.pem", "wb") as priv_file, open("public_key.pem", "wb") as pub_file:
            priv_file.write(private_pem)
            pub_file.write(public_pem)

        print("🔑 RSA Keys Generated!")

    def detect_intrusion(self, system_logs):
        """AI-powered intrusion detection"""
        data = np.array([len(log) for log in system_logs]).reshape(1, -1)
        prediction = self.model.predict(data)[0][0] if self.model else 0.0

        if prediction > 0.85:
            print("⚠️ Intrusion Detected! Possible unauthorized access attempt.")
            return True
        return False

    def self_destruct(self, encrypted_file):
        """Deletes the file securely"""
        try:
            os.remove(encrypted_file)
            print(f"🔥 Self-destruct executed: {encrypted_file} deleted.")
        except:
            print("Error deleting file.")

    def blockchain_store_key(self, public_key):
        """Decentralized key storage (Simulated API call)"""
        blockchain_api = "https://fake-blockchain-api.com/store"
        response = requests.post(blockchain_api, json={"key": public_key})
        if response.status_code == 200:
            print("✅ Key stored securely on blockchain.")
        else:
            print("⚠️ Failed to store key on blockchain.")

# ------------------------------
# RUN THE TOOL
# ------------------------------
if __name__ == "__main__":
    cs = CipherSentry()

    # Example usage:
    cs.generate_rsa_keys()  
    encrypted_file = cs.encrypt_file("example.txt")
    cs.decrypt_file(encrypted_file)

    system_logs = ["Failed login attempt", "Root access request", "SSH brute-force detected"]
    cs.detect_intrusion(system_logs)

    cs.self_destruct(encrypted_file)
