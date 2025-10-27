import itertools
import hashlib
import base64

# The base64 string with ? placeholders
template = "RkxB?19N?01P?1NJ?05BVFVSRQ=="

# The target MD5 hash
target_hash = "ac93182e124d1c843e9bcd9bec1f1797"

# Valid Base64 characters
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Find positions of '?'
positions = [i for i, c in enumerate(template) if c == '?']
print(f"Found {len(positions)} missing characters at {positions}")

# Try all possible combinations
for combo in itertools.product(chars, repeat=len(positions)):
    # Replace the ?s with the characters from this combo
    test = list(template)
    for pos, val in zip(positions, combo):
        test[pos] = val
    candidate = "".join(test)

    # Hash the candidate and compare
    if hashlib.md5(candidate.encode()).hexdigest() == target_hash:
        print("\n✅ Match found!")
        print(f"Replacements: {combo}")
        print("Base64 string:", candidate)
        print("Decoded text:", base64.b64decode(candidate).decode(errors='ignore'))
        break
else:
    print("❌ No match found.")
