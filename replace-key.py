import sys
import urllib.request


def get_minio_public_key():
    f = urllib.request.urlopen("https://subnet.min.io/downloads/license-pubkey.pem")
    public_key = f.read()
    if public_key[0:27] != b"-----BEGIN PUBLIC KEY-----\n":
        raise ValueError("wrong public key prefix")
    if public_key[-26:] != b"\n-----END PUBLIC KEY-----\n":
        raise ValueError("wrong public key suffix")
    return public_key[0:-1]


def ROL1(x, n):
    x = x & 0xFF
    n = n & 7
    if n == 0:
        return x
    return ((x << n) | (x >> (8 - n))) & 0xFF


def ROR1(x, n):
    return ROL1(x, (8 - n) & 7)


def encrypt_blob(plaintext):
    data = bytearray(plaintext)
    result = bytearray(len(data))
    state = -98
    offset = 0
    remaining = len(data)
    while remaining > 0:
        r = remaining
        s = state + 49
        if r >= 8:
            c = ROR1((data[offset + 7] ^ s ^ 0xD0) & 0xFF, 5)
            result[offset + 7] = c
            s ^= c
        s = s - 113
        if r >= 7:
            c = ROR1((data[offset + 6] ^ s ^ 0x5B) & 0xFF, 4)
            result[offset + 6] = c
            s ^= c
        s = s - 12
        if r >= 13:
            c = ROR1((data[offset + 12] ^ s ^ 0x1B) & 0xFF, 3)
            result[offset + 12] = c
            s ^= c
        s = s + 47
        if r >= 4:
            c = ROR1((data[offset + 3] ^ s ^ 0x51) & 0xFF, 2)
            result[offset + 3] = c
            s ^= c
        s = s - 125
        if r >= 5:
            c = ROR1((data[offset + 4] ^ s ^ 0xBC) & 0xFF, 1)
            result[offset + 4] = c
            s ^= c
        s = s - 102
        if r >= 6:
            c = (data[offset + 5] ^ s ^ 0xBF) & 0xFF
            result[offset + 5] = c
            s ^= c
        s = s - 81
        if r >= 12:
            c = ROR1((data[offset + 11] ^ s ^ 0x31) & 0xFF, 7)
            result[offset + 11] = c
            s ^= c
        s = s + 92
        if r >= 14:
            c = ROR1((data[offset + 13] ^ s ^ 0x11) & 0xFF, 6)
            result[offset + 13] = c
            s ^= c
        s = s + 4
        if r >= 3:
            c = ROR1((data[offset + 2] ^ s ^ 0x9D) & 0xFF, 5)
            result[offset + 2] = c
            s ^= c
        s = s - 60
        if r >= 11:
            c = ROR1((data[offset + 10] ^ s ^ 0x78) & 0xFF, 4)
            result[offset + 10] = c
            s ^= c
        s = s + 94
        c = ROR1((data[offset + 0] ^ s ^ 0x60) & 0xFF, 5)
        result[offset + 0] = c
        s = (c ^ s) - 124
        if r >= 9:
            c = ROR1((data[offset + 8] ^ s ^ 0x6C) & 0xFF, 4)
            result[offset + 8] = c
            s ^= c
        s = s - 107
        if r >= 2:
            c = ROR1((data[offset + 1] ^ s ^ 0xEA) & 0xFF, 3)
            result[offset + 1] = c
            s ^= c
        s = s + 39
        if r >= 16:
            c = ROR1((data[offset + 15] ^ s ^ 0x43) & 0xFF, 2)
            result[offset + 15] = c
            s ^= c
        s = s + 70
        if r >= 10:
            c = ROR1((data[offset + 9] ^ s ^ 0xA1) & 0xFF, 1)
            result[offset + 9] = c
            s ^= c
        state = s - 18
        if r >= 15:  # no ROL
            c = (data[offset + 14] ^ state ^ 0xCE) & 0xFF
            result[offset + 14] = c
            state ^= c
        step = min(r, 16)
        offset += step
        remaining -= step
    return bytes(result)


if len(sys.argv) < 4:
    print(
        f"Usage: ./{sys.argv[0]} <original minio binary> <new minio binary> <new public key>"
    )
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
    raise ValueError(
        f"wrong new public key length: {len(new_public_key)} != {len(original_public_key)}"
    )

new_minio_binary = minio_binary.replace(
    encrypt_blob(original_public_key), encrypt_blob(new_public_key)
)
if new_minio_binary == minio_binary:
    raise ValueError(f"could not replace old public key")

with open(new_minio_binary_path, "wb") as f:
    f.write(new_minio_binary)
