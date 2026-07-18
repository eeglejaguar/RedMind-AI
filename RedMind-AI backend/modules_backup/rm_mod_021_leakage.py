# RM-MOD-021 - Public leakage hint scanner (emails, keys in page)
id = "RM-MOD-021"
name = "Public Leakage Hints"
description = "Search public HTML for email-like strings, 'password', 'apikey' hints (only scanning public page)."

def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = (r.text or "")[:5000]
        emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', body)
        hints = []
        for kw in ["password","passwd","api_key","apikey","secret","private_key","credential"]:
            if kw in body.lower():
                hints.append(kw)
        return {"target": target, "status_code": r.status_code, "emails": list(set(emails)), "hints": hints, "snippet": body[:500]}
    except Exception as e:
        return {"target": target, "error": str(e)}
