import requests
import time

def run(target, timeout=15, dangerous=False):
    results = []
    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    endpoints = ["/setup","/admin/setup","/install","/initialize","/api/setup"]
    for ep in endpoints:
        try:
            r = requests.get(target.rstrip("/") + ep, headers=headers, timeout=timeout)
            if r.status_code == 200:
                results.append({
                    "endpoint": ep,
                    "status": r.status_code,
                    "confidence": "HIGH",
                    "evidence": r.text[:150]
                })
        except Exception:
            pass


    return {
        "check_id": "RM-CHK-016",
        "severity": "CRITICAL",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {
            "tested_requests": len(results),
            "positive_hits": len(results)
        }
    }
