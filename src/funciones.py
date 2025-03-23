import random
import string
import hashlib

def hash_text(text):
    encoded_text = text.encode()
    hash_object = hashlib.sha256(encoded_text)
    hash_hex = hash_object.hexdigest()
    return hash_hex

def generar_clave(longitud=32):
    """Genera una clave aleatoria de longitud especificada."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    clave = ''.join(random.choice(caracteres) for _ in range(longitud))
    return clave

def xor_encrypt_decrypt(text, key):
    #  Encriptar o desencriptar texto usando XOR
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

if __name__ == "__main__":
    # Test the generar_clave function
    clave_maestra = generar_clave()
    key = "patatito"
    encrypted = xor_encrypt_decrypt(clave_maestra, key)
    decrypted = xor_encrypt_decrypt(encrypted, key)
    print(f"Clave maestra generada: {clave_maestra}")

    print(f"Encrypted text: {encrypted}")
    print(f"Decrypted text: {decrypted}")
 