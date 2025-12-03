import base64, pyotp, datetime

seed = open("/data/seed.txt").read().strip()
seed_bytes = bytes.fromhex(seed)
base32_seed = base64.b32encode(seed_bytes).decode()

totp = pyotp.TOTP(base32_seed)
code = totp.now()

ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
print(f"{ts} - 2FA Code: {code}")
