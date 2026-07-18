import requests
import time

def run(target, timeout=15, dangerous=False):
    results = []
    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    try:
        r1 = requests.get(target + "/1", headers=headers, timeout=timeout)
        r2 = requests.get(target + "/2", headers=headers, timeout=timeout)
        if r1.status_code == 200 and r2.status_code == 200:
            results.append({
                "issue": "Potential IDOR",
                "confidence": "MEDIUM"
            })
    except Exception:
        pass


    return {
        "check_id": "RM-CHK-072",
        "severity": "HIGH",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {
            "tested_requests": len(results),
            "positive_hits": len(results)
        }
    }
