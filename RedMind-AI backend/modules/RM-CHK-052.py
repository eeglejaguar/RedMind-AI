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
        cookies = r.headers.get("Set-Cookie","")
        if "HttpOnly" not in cookies or "Secure" not in cookies:
            results.append({
                "issue": "Weak session cookie flags",
                "confidence": "MEDIUM",
                "evidence": cookies
            })
    except Exception:
        pass


    return {
        "check_id": "RM-CHK-052",
        "severity": "HIGH",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {
            "tested_requests": len(results),
            "positive_hits": len(results)
        }
    }
