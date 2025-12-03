# request_seed.py
import json
import requests

def _pem_to_json_field(pem_bytes: bytes) -> str:
    return pem_bytes.decode("utf-8").strip()  # FIXED

def request_seed(student_id: str, github_repo_url: str, 
                 api_url: str = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws", 
                 public_pem_path: str = "student_public.pem", timeout: int = 15):
    
    with open(public_pem_path, "rb") as f:
        public_pem_bytes = f.read()

    public_key_field = _pem_to_json_field(public_pem_bytes)

    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_field
    }

    headers = {"Content-Type": "application/json"}
    resp = requests.post(api_url, json=payload, headers=headers, timeout=timeout)

    print("\n📩 Raw API Response:", resp.text)

    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "success":
        raise RuntimeError(f"❌ API Error: {data}")

    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        raise RuntimeError("❌ Missing encrypted_seed in response.")

    with open("encrypted_seed.txt", "w") as out:
        out.write(encrypted_seed)

    print("\n✅ Encrypted seed saved to encrypted_seed.txt (DO NOT COMMIT THIS FILE).")
    return encrypted_seed
