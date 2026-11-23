
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


KEY_DIR = Path("keys")
PUBLIC_KEY_FILE = KEY_DIR / "public_key.pem"
PRIVATE_KEY_FILE = KEY_DIR / "private_key.pem"


# generating RSA Key Pair
def generate_keys():

    KEY_DIR.mkdir(exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    # save public key
    with open(PUBLIC_KEY_FILE, "wb") as file:
        file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    # save private key
    with open(PRIVATE_KEY_FILE, "wb") as file:
        file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    print("RSA key pair generated and saved.")


# load RSA Keys
def load_keys():

    with open(PUBLIC_KEY_FILE, "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())

    with open(PRIVATE_KEY_FILE, "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )

    return public_key, private_key


# RSA Encryption
def encrypt(message, public_key):

    ciphertext = public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext


# RSA Decryption
def decrypt(ciphertext, private_key):

    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode("utf-8")


# Digital Signature generation
def sign_message(message, private_key):

    signature = private_key.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


# Digital Signature verification
def verify_signature(message, signature, public_key):

    try:
        public_key.verify(
            signature,
            message.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except Exception:
        return False


# Main Execution
def main():

    print("=" * 50)
    print("          RSA CRYPTOSYSTEM")
    print("=" * 50)

    generate_keys()

    public_key, private_key = load_keys()

    message = input("\nEnter a message: ")

    # Encryption
    ciphertext = encrypt(message, public_key)

    print("\nCiphertext:", ciphertext.hex())

    # Digital signature
    signature = sign_message(message, private_key)

    print("\nDigital Signature:", signature.hex())

    # Decryption
    try:
        plaintext = decrypt(ciphertext, private_key)
        print("\nDecrypted Message:", plaintext)

    except Exception:
        plaintext = None
        print("\nDecryption failed.")

    # Signature verification
    if plaintext is not None and verify_signature(
        plaintext, signature, public_key
    ):
        print("\nSignature verified successfully.")

    else:
        print("\nSignature verification failed.")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
