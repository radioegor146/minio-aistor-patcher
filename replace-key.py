import sys
import urllib.request

def get_minio_public_key():
    f = urllib.request.urlopen("https://subnet.min.io/downloads/license-pubkey.pem")
    public_key = f.read()
    if public_key[0:27] != b'-----BEGIN PUBLIC KEY-----\n':
        raise ValueError("wrong public key prefix")
    if public_key[-26:] != b'\n-----END PUBLIC KEY-----\n':
        raise ValueError("wrong public key suffix")
    return public_key[0:-1]

if len(sys.argv) < 4:
    print(f"Usage: ./{sys.argv[0]} <original minio binary> <new minio binary> <new public key>")
    exit(1)

original_minio_binary_path = sys.argv[1]
new_minio_binary_path = sys.argv[2]
new_public_key_path = sys.argv[3]

with open(original_minio_binary_path, "rb") as f:
    minio_binary = f.read()

original_public_key = get_minio_public_key()

with open(new_public_key_path, "r") as f:
    new_public_key = f.read().strip().encode("ascii")

if len(new_public_key) != len(original_public_key):
    raise ValueError(f"wrong new public key length: {len(new_public_key)} != {len(original_public_key)}")

new_minio_binary = minio_binary.replace(original_public_key, new_public_key)
if new_minio_binary == minio_binary:
    raise ValueError(f"could not replace old public key")

with open(new_minio_binary_path, "wb") as f:
    f.write(new_minio_binary)