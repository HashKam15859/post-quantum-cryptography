
import secrets
from math import gcd


# 1. Miller-Rabin Primality Test
def is_prime(n, rounds=40):

    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    for prime in small_primes:
        if n % prime == 0:
            return n == prime

    # Express n - 1 as 2^s * d, where d is odd
    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    # Perform Miller-Rabin rounds
    for _ in range(rounds):

        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break

        else:
            return False

    return True


# 2. Generate a Random Prime Number
def generate_prime(bits=512):

    while True:

        candidate = secrets.randbits(bits)

        # Ensure the candidate has exactly 'bits' bits
        # and is odd
        candidate |= (1 << (bits - 1)) | 1

        if is_prime(candidate):
            return candidate


# 3. Calculate Euler's Totient Function
def euler_totient(p, q):
    return (p - 1) * (q - 1)


# 4. Extended Euclidean Algorithm
def extended_gcd(a, b):

    if b == 0:
        return a, 1, 0

    gcd_value, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return gcd_value, x, y


# 5. Calculate Modular Multiplicative Inverse
def modular_inverse(e, phi):

    gcd_value, x, _ = extended_gcd(e, phi)

    if gcd_value != 1:
        raise ValueError("Modular inverse does not exist.")

    return x % phi


# 6. RSA Key Generation
def generate_keys(bits=512):

    e = 65537

    while True:

        p = generate_prime(bits)
        q = generate_prime(bits)

        if p == q:
            continue

        n = p * q

        phi = euler_totient(p, q)

        if gcd(e, phi) == 1:
            break

    d = modular_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


# 7. RSA Encryption
def encrypt(message, public_key):

    e, n = public_key
    ciphertext = []

    for char in message:

        m = ord(char)

        if m >= n:
            raise ValueError("Character exceeds RSA modulus.")

        c = pow(m, e, n)
        ciphertext.append(c)

    return ciphertext


# 8. RSA Decryption
def decrypt(ciphertext, private_key):

    d, n = private_key
    plaintext = ""

    for c in ciphertext:

        if not 0 <= c < n:
            raise ValueError("Invalid ciphertext value.")

        m = pow(c, d, n)
        plaintext += chr(m)

    return plaintext


# 9. Main Execution
def main():

    print("=" * 50)
    print("          RSA MATHEMATICAL IMPLEMENTATION")
    print("=" * 50)

    print("\nGenerating RSA key pair...")

    public_key, private_key = generate_keys()

    print("\nKey Generation Successful!")
    print("Public Key :", public_key)
    print("Private Key:", private_key)

    message = input("\nEnter plaintext: ")

    # Encryption
    ciphertext = encrypt(message, public_key)

    print("\nEncrypted Ciphertext:")
    print(ciphertext)

    # Decryption
    decrypted_message = decrypt(ciphertext, private_key)

    print("\nDecrypted Plaintext:")
    print(decrypted_message)

    # Verification
    print("\nVerification:")

    if decrypted_message == message:
        print("SUCCESS: Original and decrypted messages match.")
    else:
        print("FAILURE: Message verification failed.")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
