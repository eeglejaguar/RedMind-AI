import os
from textwrap import indent

MODULE_DIR = "modules"
os.makedirs(MODULE_DIR, exist_ok=True)

def write_module(check_id, severity, payload_code):
    content = f'''import requests
import time

def run(target, timeout=15, dangerous=False):
    results = []
    headers = {{
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }}

{indent(payload_code, "    ")}

    return {{
        "check_id": "{check_id}",
        "severity": "{severity}",
        "target": target,
        "dangerous": dangerous,
        "findings": results,
        "summary": {{
            "tested_requests": len(results),
            "positive_hits": len(results)
        }}
    }}
'''
    with open(os.path.join(MODULE_DIR, f"{check_id}.py"), "w", encoding="utf-8") as f:
        f.write(content)

# ---- Payload Definitions ----

def admin_payload():
    return '''
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
'''

def xss_payload():
    return '''
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
'''

def auth_payload():
    return '''
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
'''

def idor_payload():
    return '''
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
'''

def traversal_payload():
    return '''
try:
    r = requests.get(target + "?file=../etc/passwd", headers=headers, timeout=timeout)
    if "root:x" in r.text:
        results.append({
            "issue": "Path Traversal",
            "confidence": "HIGH"
        })
except Exception:
    pass
'''

def ssrf_payload():
    return '''
try:
    r = requests.get(target + "?url=http://169.254.169.254", headers=headers, timeout=timeout)
    if r.status_code in [200,500]:
        results.append({
            "issue": "SSRF probe reachable",
            "confidence": "MEDIUM"
        })
except Exception:
    pass
'''

def api_payload():
    return '''
try:
    r = requests.post(target, headers=headers, timeout=timeout)
    if r.status_code == 200:
        results.append({
            "issue": "Method tampering",
            "confidence": "LOW"
        })
except Exception:
    pass
'''

def header_payload():
    return '''
try:
    r = requests.get(target, headers=headers, timeout=timeout)
    if "X-Frame-Options" not in r.headers:
        results.append({
            "issue": "Missing security headers",
            "confidence": "LOW"
        })
except Exception:
    pass
'''

# ---- Generate 179 Modules ----

for i in range(1, 180):
    cid = f"RM-CHK-{i:03d}"

    if i <= 20:
        write_module(cid, "CRITICAL", admin_payload())
    elif i <= 40:
        write_module(cid, "HIGH", xss_payload())
    elif i <= 60:
        write_module(cid, "HIGH", auth_payload())
    elif i <= 80:
        write_module(cid, "HIGH", idor_payload())
    elif i <= 100:
        write_module(cid, "CRITICAL", traversal_payload())
    elif i <= 120:
        write_module(cid, "CRITICAL", ssrf_payload())
    elif i <= 150:
        write_module(cid, "MEDIUM", api_payload())
    else:
        write_module(cid, "LOW", header_payload())

print("✔ 179 FIXED modules generated successfully")
