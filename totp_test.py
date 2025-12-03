import base64, pyotp

hex_seed = open("seed.txt").read().strip()
seed_bytes = bytes.fromhex(hex_seed)
base32_seed = base64.b32encode(seed_bytes).decode()

totp = pyotp.TOTP(base32_seed)
print("TOTP:", totp.now())
