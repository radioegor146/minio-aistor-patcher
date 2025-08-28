import sys
import jwcrypto.jwk
import jwcrypto.jwt

if len(sys.argv) < 3:
    print(f"Usage: ./{sys.argv[0]} <private key> <output license file>")
    exit(1)

private_key_path = sys.argv[1]
output_license_file = sys.argv[2]

with open(private_key_path, "rb") as f:
    private_key = jwcrypto.jwk.JWK.from_pem(f.read())

jwt_data = {
    "sub": "acme@min.io",
    "exp": 2000000000,
    "iss": "subnet@min.io",
    "iat": 0,
    "aid": 1337,
    "org": "acme",
    "cap": 1000000000,
    "plan": "STANDARD"
}

license_jwt = jwcrypto.jwt.JWT(claims=jwt_data, header={
    "alg": "ES384",
    "typ": "JWT"
})
license_jwt.make_signed_token(private_key)

with open(sys.argv[2], "w") as f:
    f.write(license_jwt.serialize())