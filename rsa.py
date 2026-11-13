import random
from math import gcd

def is_prime(n):
    if n<2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n%i==0:
            return False
    return True 

def gen_prime():
    while True:
        n = random.randint(100,300)
        if is_prime(n):
            return n
        
def gen_keys():
    p = gen_prime()
    q = gen_prime()
    while p==q: 
        q = gen_prime()
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    if gcd(e, phi) != 1:
        return gen_keys()
    d = pow(e, -1, phi)
    public_key = (e, n)
    private_key = (d, n)
        
    return public_key, private_key
    
def encrypt(message, public_key):
    e, n = public_key
    cipher = []
    
    for char in message:
        encrypt_char = pow(ord(char), e, n)
        cipher.append(encrypt_char)
        
    return cipher

def decrypt(cipher, private_key):
    
    d, n= private_key
    decrypt_mssg = ""
    for value in cipher: 
        decrypt_char = pow(value, d, n)
        decrypt_mssg += chr(decrypt_char)
    return decrypt_mssg

def main():
    print("RSA Encryption")
    public_key, private_key = gen_keys()
    print("Public key: ", public_key)
    print("Private key: ", private_key)
    msg = input("Enter a message to encrypt: ")
    cipher = encrypt(msg, public_key)
    print("Encrypted message: ", cipher)
    decrypt_msg = decrypt(cipher, private_key)
    print("Decrypted Message: ", decrypt_msg)
    
if __name__ == "__main__":
     main()
