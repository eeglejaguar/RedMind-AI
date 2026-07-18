import requests
import time

def run(target, timeout=15, dangerous=False):
    results = []
    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    try:
        r = requests.get(target + "?url=http://169.254.169.254", headers=headers, timeout=timeout)
        if r.status_code in [200,500]:
            results.append({
                "issue": "SSRF probe reachable",
                "confidence": "MEDIUM"
            })
    except Exception:
        pass


    return {
        "check_id": "RM-CHK-102",
        "severity": "CRITICAL",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {
            "tested_requests": len(results),
            "positive_hits": len(results)
        }
    }
