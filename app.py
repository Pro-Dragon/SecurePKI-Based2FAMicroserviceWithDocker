from fastapi import FastAPI, HTTPException
import os, base64, pyotp, time
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = FastAPI()
DATA_PATH = "/data/seed.txt"

@app.post("/decrypt-seed")
def decrypt_seed_api(data: dict):
    try:
        encrypted_b64 = data["encrypted_seed"]

        with open("student_private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        cipher_bytes = base64.b64decode(encrypted_b64)
        seed = private_key.decrypt(
            cipher_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

        os.makedirs("/data", exist_ok=True)
        with open(DATA_PATH, "w") as f:
            f.write(seed)

        return {"status": "ok"}
    except:
        raise HTTPException(500, "Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(500, "Seed not decrypted yet")

    seed = open(DATA_PATH).read().strip()
    seed_bytes = bytes.fromhex(seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    valid_for = 30 - int(time.time()) % 30

    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa(data: dict):
    if "code" not in data:
        raise HTTPException(400, "Missing code")

    if not os.path.exists(DATA_PATH):
        raise HTTPException(500, "Seed not decrypted yet")

    seed = open(DATA_PATH).read().strip()
    seed_bytes = bytes.fromhex(seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    valid = totp.verify(data["code"], valid_window=1)

    return {"valid": valid}
