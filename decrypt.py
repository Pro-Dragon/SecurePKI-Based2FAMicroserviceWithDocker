import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("encrypted_seed.txt") as f:
    encrypted_b64 = f.read()

cipher_bytes = base64.b64decode(encrypted_b64)

seed = private_key.decrypt(
    cipher_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
).decode()

print("Seed:", seed)
