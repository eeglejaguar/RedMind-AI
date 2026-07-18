id="RM-MOD-054"
name="Password Reset / Token Hints"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = (r.text or "")[:3000]
        hints=[]
        for p in [r"reset_password", r"password_reset", r"token="]:
            if re.search(p, body, re.I):
                hints.append(p)
        return {"target": target, "status": r.status_code, "hints": hints}
    except Exception as e:
        return {"target": target, "error": str(e)}
