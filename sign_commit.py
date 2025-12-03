import base64, subprocess
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

commit_hash = subprocess.getoutput("git log -1 --format=%H")

private_key = serialization.load_pem_private_key(
    open("student_private.pem", "rb").read(), password=None)

signature = private_key.sign(
    commit_hash.encode(),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

instructor_pub = serialization.load_pem_public_key(
    open("instructor_public.pem", "rb").read()
)

encrypted = instructor_pub.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(base64.b64encode(encrypted).decode())
