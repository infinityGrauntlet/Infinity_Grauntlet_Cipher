# Written by - Krish Hazarika 10376173
# ChatGPT was used to fix logical and syntax errors. 

import random

def substitution(byte, key):
    """ Perform byte substitution using the key """
    byte = byte^key
    return ((byte >> 4) & 0xF) | ((byte << 4) & 0xF0)

def permutation(block, key):
    """ Use the key to create a random permutation of the block """
    random.seed(key)
    # Create a list of indexes for the block
    indexes = list(range(len(block)))
    # Shuffle the list
    random.shuffle(indexes)
    # Use the shuffled list to create the permutation of the block
    shuffled_block = bytearray([block[i] for i in indexes])
    return shuffled_block

def encrypt_block(block, key):
    """ Encrypt a block using 16 rounds of key addition, permutation, and substitution """
    for i in range(16):
        block = bytearray([substitution(byte, key[i]) for byte in block])
        block = permutation(block, key[i])
        block = key_addition(block, key[i])
    return block

def decrypt_block(block, key):
    """ Decrypt a block using 16 rounds in reverse order for decryption """
    for i in reversed(range(16)):
        block = key_subtraction(block, key[i])
        block = permutation_inverse(block, key[i])
        block = bytearray([substitution_inverse(byte, key[i]) for byte in block])
    return block

def key_addition(block, key):
    """ Add the key to the block using XOR """
    result = bytearray(len(block))
    for i in range(len(block)):
        result[i] = block[i]^key
    return result

def key_subtraction(block, key):
    """ Reverse key addition by subtracting the key from the block """
    return key_addition(block, key)

def permutation_inverse(block, key):
    """ Reverse the permutation of the block """
    random.seed(key)
    # Create a list of indexes for the block
    indexes = list(range(len(block)))
    # Shuffle the list
    random.shuffle(indexes)
    # Use the shuffled list to create the original order of the block
    inverted_indexes = [0] * len(indexes)
    for i, index in enumerate(indexes):
        inverted_indexes[index] = i
    # Use the inverted list to create the original block
    original_block = bytearray([block[i] for i in inverted_indexes])
    return original_block

def substitution_inverse(byte, key):
    """ Reverse the byte substitution using the key """
    byte = ((byte >> 4) & 0xF) | ((byte << 4) & 0xF0)
    byte = byte^key
    return byte

def pad_block(block):
    """ Add PKCS#7 padding to the block """
    padding_len = 16 - (len(block) % 16)
    padding = bytearray([padding_len]*padding_len)
    return block + padding

def unpad_block(padded_block):
    """ Remove PKCS#7 padding from the block """
    padding_len = padded_block[-1]
    return padded_block[:-padding_len]

def encrypt_message(message, key):
    """ Encrypt the message using AES encryption algorithm with 128-bit key """
    key = bytearray(key)
    padded_message = pad_block(message.encode())
    ciphertext = bytearray()
    for i in range(0, len(padded_message), 16):
        block = encrypt_block(padded_message[i:i+16], key)
        ciphertext += block
    return bytes(ciphertext)

def decrypt_message(ciphertext, key):
    """ Decrypt the message using AES decryption algorithm with 128-bit key """
    key = bytearray(key)
    plaintext = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = decrypt_block(ciphertext[i:i+16], key)
        if len(block) != 16:
            print("Error: block size is not 16")
            return ''
        plaintext += block
    unpadded_plaintext = unpad_block(plaintext)
    return unpadded_plaintext.decode()

# Generate a random key
key = [random.randint(0, 255) for i in range(16)]

# Encrypt and decrypt a message
plaintext = "Leave the pendrive in building 18.203"
ciphertext = encrypt_message(plaintext, key)
print("Ciphertext:", ciphertext)
decrypted_plaintext = decrypt_message(ciphertext, key)
print("Decrypted plaintext:", decrypted_plaintext)

