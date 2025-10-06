# Natas16 → Natas17

## Overview
This level demonstrates a blind command-injection / command execution technique via a search input on the Natas16 web page.  
The objective is to retrieve the password for `natas17` which is stored on the server at `/etc/natas_webpass/natas17`.

---

## Approach
1. The web application accepts a `needle` parameter and runs a server-side command that can be influenced by input.
2. By injecting a command that calls `grep` on `/etc/natas_webpass/natas17`, we can test whether the file contains strings that start with a chosen prefix.
3. This is done blind: we infer matches from differences in the page output (e.g., presence/absence of an injected marker like `zooming`).
4. Enumerate the password character-by-character by guessing each next character from a defined charset.

Example of the injection pattern used to test whether the password begins with `PREFIX+X`:
If `grep` finds a line matching `^PREFIXX`, the server output will differ (which the script detects).

---

## Usage
1. Set your credentials:
```python
python3 natas16.py --user natas16 --pass LEVEL_PASSWORD

