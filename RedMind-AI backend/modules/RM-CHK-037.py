import requests
import time

def run(target, timeout=15, dangerous=False):
    results = []
    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    payload = "<script>alert(1)</script>"
    try:
        r = requests.get(target + "?q=" + payload, headers=headers, timeout=timeout)
        if payload in r.text:
            results.append({
                "vector": "reflected",
                "confidence": "HIGH",
                "evidence": payload
            })
    except Exception:
        pass


    return {
        "check_id": "RM-CHK-037",
        "severity": "HIGH",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {
            "tested_requests": len(results),
            "positive_hits": len(results)
        }
    }
