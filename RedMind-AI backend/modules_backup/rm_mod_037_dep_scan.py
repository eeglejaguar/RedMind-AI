# rm_mod_037_dep_scan.py
import requests
import re
import json
import sys
import argparse

def scan_target(target_url):
    result = {
        "target": target_url,
        "status": None,
        "candidates_inspected": 0,
        "libraries": [],
        "raw_findings_count": 0
    }

    try:
        # Fetch target page
        r = requests.get(target_url, timeout=5)
        result["status"] = r.status_code
        body = r.text

        # Find <script src="..."> tags
        scripts = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', body, re.I)
        result["candidates_inspected"] = len(scripts)
        result["raw_findings_count"] = len(scripts)

        for src in scripts:
            lib = {"src": src, "local_status": None, "cdn_status": None}
            try:
                # Try fetching locally (if relative URL)
                if src.startswith("http"):
                    local_url = src
                else:
                    local_url = target_url.rstrip("/") + "/" + src.lstrip("/")
                r_local = requests.get(local_url, timeout=5)
                lib["local_status"] = r_local.status_code
            except Exception as e:
                lib["local_status"] = "error"

            # Try fetching CDN version (if src points to a known CDN URL)
            if "cdnjs" in src or "jsdelivr" in src or "unpkg" in src:
                try:
                    r_cdn = requests.get(src, timeout=5)
                    lib["cdn_status"] = r_cdn.status_code
                except Exception as e:
                    lib["cdn_status"] = "error"

            result["libraries"].append(lib)

    except Exception as e:
        result["error"] = str(e)

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dependency Scan Module")
    parser.add_argument("--target", required=True, help="Target URL to scan")
    args = parser.parse_args()

    scan_result = scan_target(args.target)
    print(json.dumps(scan_result, indent=4))
