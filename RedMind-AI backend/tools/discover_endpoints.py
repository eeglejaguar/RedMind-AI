#!/usr/bin/env python3
# tools/discover_endpoints.py
import argparse, requests, sys, time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True, help="Base URL to crawl")
parser.add_argument("--max-pages", type=int, default=30, help="Maximum pages to crawl")
args = parser.parse_args()
base = args.target.rstrip("/")
session = requests.Session()
session.headers.update({"User-Agent": "RedMind-Discovery/1.0"})

def same_domain(url):
    try:
        return urlparse(url).netloc == urlparse(base).netloc
    except:
        return False

seen = set()
to_visit = [base]
discovered_links = []
forms = []

while to_visit and len(seen) < args.max_pages:
    url = to_visit.pop(0)
    if url in seen:
        continue
    seen.add(url)
    try:
        r = session.get(url, timeout=10)
    except Exception as e:
        print(f"ERROR fetching {url}: {e}")
        continue
    print(f"FETCH {url} -> {r.status_code} (len {len(r.text)})")
    soup = BeautifulSoup(r.text, "lxml")
    # links
    for a in soup.find_all("a", href=True):
        href = a['href'].strip()
        full = urljoin(url, href)
        if same_domain(full) and full not in seen and full not in to_visit:
            to_visit.append(full)
        discovered_links.append(full)
    # forms
    for f in soup.find_all("form"):
        action = f.get("action") or ""
        method = (f.get("method") or "get").lower()
        fullact = urljoin(url, action)
        inputs = []
        for inp in f.find_all(["input","textarea","select"]):
            name = inp.get("name")
            if name:
                inputs.append(name)
        forms.append({"page": url, "action": fullact, "method": method, "inputs": inputs})
    # polite delay
    time.sleep(0.2)

# Deduplicate and print results
print("\n=== DISCOVERED LINKS ===")
for l in sorted(set(discovered_links)):
    print(l)

print("\n=== DISCOVERED FORMS ===")
for f in forms:
    print(f"- page: {f['page']}")
    print(f"  action: {f['action']}")
    print(f"  method: {f['method']}")
    print(f"  inputs: {f['inputs']}\n")

print("Done. Use the 'action' and 'inputs' values to update module payload paths/params.")
