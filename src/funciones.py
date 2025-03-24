import random
import string
import hashlib
import os
import shutil

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

def almacenar_pdf(pdf_path, key):
    # Define the target directory
    target_directory = '../data/pdf'
    
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    # Get the filename from the provided path
    filename = os.path.basename(pdf_path)
    
    # Define the target path for the encrypted PDF
    target_path = os.path.join(target_directory, filename + '.enc')  # Save as .enc for encrypted file
    
    # Read the PDF file as binary
    with open(pdf_path, 'rb') as file:
        pdf_data = file.read()
    
    # Encrypt the PDF data
    encrypted_data = xor_encrypt_decrypt(pdf_data.decode('latin-1'), key)  # Decode to string for XOR
    
    # Save the encrypted data to the target path
    with open(target_path, 'wb') as file:
        file.write(encrypted_data.encode('latin-1'))  # Encode back to bytes for saving
    
    return target_path


def descargar_pdf(encrypted_pdf_path, key, output_path=None):
    # Set default output path to the user's Downloads directory if not provided
    if output_path is None:
        output_path = os.path.join(os.path.expanduser("~"), "Downloads", os.path.basename(encrypted_pdf_path[:-4]))  # Remove .enc extension
    
    # Read the encrypted PDF file as binary
    with open(encrypted_pdf_path, 'rb') as file:
        encrypted_data = file.read()
    
    # Decrypt the PDF data
    decrypted_data = xor_encrypt_decrypt(encrypted_data.decode('latin-1'), key)  # Decode to string for XOR
    
    # Save the decrypted data to the specified output path
    with open(output_path, 'wb') as file:
        file.write(decrypted_data.encode('latin-1'))  # Encode back to bytes for saving
    
    return output_path
if __name__ == "__main__":
    # Test the generar_clave function
    # almacenar_pdf("../Git-Cheat-Sheet-EN.pdf","patatito")
    # Path to the encrypted PDF file
    encrypted_pdf_path = '../data/pdf/Git-Cheat-Sheet-EN.pdf.enc'

    # Sample key for decryption (use the same key that was used for encryption)
    decryption_key = 'patatito'  # Replace with the actual key used

    # Call the descargar_pdf function
    descargar_pdf(encrypted_pdf_path, decryption_key)
 