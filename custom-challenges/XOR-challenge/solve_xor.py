#!/usr/bin/env python3
"""
xor_solver.py
--------------
A simple script to solve repeating-key XOR challenges
when you know part of the plaintext (known-plaintext attack).

Edit CIPHERTEXT_HEX and KNOWN_PLAINTEXT to your challenge values.
"""

from math import ceil

# === INPUTS ===
CIPHERTEXT_HEX = "1e161e1b37045a18132e041a250a0941722415170e190c03370e4d1d3b1a1f095b6b360c2a220c2b3b0e"
KNOWN_PLAINTEXT = "System breached. MomoRizza rises: "
# ==============


def hex_to_bytes(hex_string):
    """Convert hex string to raw bytes."""
    return bytes.fromhex(hex_string)


def xor_bytes(data1, data2):
    """XOR two byte strings (stop at the shortest length)."""
    return bytes(a ^ b for a, b in zip(data1, data2))


def find_repeating_key_pattern(key_fragment):
    """Find the smallest repeating pattern inside the key fragment."""
    n = len(key_fragment)
    for size in range(1, n + 1):
        # If repeating the first 'size' bytes recreates the full fragment
        if (key_fragment[:size] * ceil(n / size))[:n] == key_fragment:
            return key_fragment[:size]
    return key_fragment


def repeat_key_to_length(key, total_length):
    """Repeat the key until it reaches the required total length."""
    return (key * ceil(total_length / len(key)))[:total_length]


# --- Step 1: Convert data to bytes ---
cipher_bytes = hex_to_bytes(CIPHERTEXT_HEX)
known_bytes = KNOWN_PLAINTEXT.encode()

# --- Step 2: Recover part of the secret key using known plaintext ---
key_fragment = xor_bytes(cipher_bytes[:len(known_bytes)], known_bytes)

# --- Step 3: Guess the smallest repeating pattern (the actual secret key) ---
recovered_key = find_repeating_key_pattern(key_fragment)

# --- Step 4: Decrypt the ciphertext using the recovered key ---
full_key = repeat_key_to_length(recovered_key, len(cipher_bytes))
decrypted_bytes = xor_bytes(cipher_bytes, full_key)
plaintext = decrypted_bytes.decode(errors="replace")

# --- Output results ---
print("=== XOR Challenge Solver ===")
print(f"Recovered key fragment: {key_fragment}")
print(f"Detected repeating key: {recovered_key.decode(errors='replace')}")
print("\nDecrypted message:")
print(plaintext)

# Try to print the flag if it looks like one
if ":" in plaintext:
    possible_flag = plaintext.split(":")[-1].strip()
    print(f"\nPossible flag → {possible_flag}")
