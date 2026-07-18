import requests
import time

def run(target, timeout=15, dangerous=False):
    results = []
    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    try:
        r = requests.get(target, headers=headers, timeout=timeout)
        if "X-Frame-Options" not in r.headers:
            results.append({
                "issue": "Missing security headers",
                "confidence": "LOW"
            })
    except Exception:
        pass


    return {
        "check_id": "RM-CHK-152",
        "severity": "LOW",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {
            "tested_requests": len(results),
            "positive_hits": len(results)
        }
    }
