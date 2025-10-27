# 🧩 Broken Base64 — Challenge Overview

This challenge presents a **partially corrupted Base64-encoded string**, where several characters have been replaced with question marks (`?`). The task is to recover the original Base64 data by finding the correct missing characters that produce a specific **MD5 hash**. Once correctly reconstructed, decoding the Base64 reveals the flag.

---

## 🧠 Concept

* **Base64 Encoding:** Converts binary data into an ASCII string using a limited character set.
* **MD5 Hashing:** A one-way hash function used here to verify correctness — only one Base64 reconstruction will match the provided hash.
* **Brute Force Search:** Since only a few characters are missing, it’s computationally feasible to iterate through all possible combinations from the Base64 alphabet.

---

## 💡 Challenge Details

* File: `index.html` (contains the challenge interface)
* Category: Cryptography
* Difficulty: Easy–Medium

The HTML file gives:

1. A **Base64 template** with missing characters.
2. A **target MD5 hash** to verify correctness.

---


## ✅ Solution Summary

When solved correctly, decoding the reconstructed Base64 string reveals:

```
FLAG_MOMO_SIGNATURE
```

