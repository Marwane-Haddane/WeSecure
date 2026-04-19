import hashlib
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def hash_text(text, algorithm="sha256", key=None):
    """Hash text using SHA-256 or PBKDF2."""
    if algorithm == "sha256":
        h = hashlib.sha256()
        h.update(text.encode('utf-8'))
        return h.hexdigest()
    elif algorithm == "pbkdf2":
        # PBKDF2 needs salt and iterations (we'll generate standard salt and prepend to output)
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key_bytes = kdf.derive(text.encode('utf-8'))
        # Return Salt + Hash encoded in base64 so it can be verified later if needed
        return base64.b64encode(salt + key_bytes).decode('utf-8')
    else:
        return f"Error: Unsupported hashing algorithm {algorithm}"

def generate_key():
    """Generates a Fernet key."""
    return Fernet.generate_key().decode()

def encrypt_text(text, algorithm, key):
    """Symmetric/Asymmetric Encryption."""
    data = text.encode('utf-8')
    try:
        if algorithm == "fernet":
            f = Fernet(key.encode('utf-8'))
            return f.encrypt(data).decode('utf-8')
            
        elif algorithm == "aes_gcm":
            # For AES GCM the key must be 16, 24 or 32 bytes long. Let's hash their key to derive a 32 byte key.
            digest = hashlib.sha256(key.encode('utf-8')).digest()
            aesgcm = AESGCM(digest)
            nonce = os.urandom(12) # Standard AES GCM nonce length
            ct = aesgcm.encrypt(nonce, data, None)
            # Prepend nonce for decryption
            return base64.b64encode(nonce + ct).decode('utf-8')
            
        elif algorithm == "rsa":
            # Assume user provided a PEM formatted public key
            public_key = serialization.load_pem_public_key(
                key.encode('utf-8'),
                backend=default_backend()
            )
            ciphertext = public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return base64.b64encode(ciphertext).decode('utf-8')
        else:
             return f"Error: Unsupported encryption algorithm {algorithm}"
    except Exception as e:
        return f"Encryption Error: {str(e)}"

def decrypt_text(text, algorithm, key):
    """Symmetric/Asymmetric Decryption."""
    try:
        if algorithm == "fernet":
            f = Fernet(key.encode('utf-8'))
            return f.decrypt(text.encode('utf-8')).decode('utf-8')
            
        elif algorithm == "aes_gcm":
            raw_data = base64.b64decode(text.encode('utf-8'))
            nonce = raw_data[:12]
            ct = raw_data[12:]
            digest = hashlib.sha256(key.encode('utf-8')).digest()
            aesgcm = AESGCM(digest)
            pt = aesgcm.decrypt(nonce, ct, None)
            return pt.decode('utf-8')
            
        elif algorithm == "rsa":
            raw_cipher = base64.b64decode(text.encode('utf-8'))
            private_key = serialization.load_pem_private_key(
                key.encode('utf-8'),
                password=None,
                backend=default_backend()
            )
            plaintext = private_key.decrypt(
                raw_cipher,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return plaintext.decode('utf-8')
        else:
             return f"Error: Unsupported decryption algorithm {algorithm}"
    except Exception as e:
        return f"Decryption Error: {str(e)}"

def process_encoding(text, algorithm, decode=False):
    """Encode/Decode purely using Base64."""
    try:
        if algorithm == "base64":
            if decode:
                return base64.b64decode(text.encode('utf-8')).decode('utf-8')
            else:
                return base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return f"Error: Unsupported encoding {algorithm}"
    except Exception as e:
        return f"Encoding/Decoding Error: {str(e)}"
