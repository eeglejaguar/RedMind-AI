id="RM-MOD-049"
name="JS Comments RCE-like Hints"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        hints = []
        for p in [r"exec\(", r"child_process", r"spawn\(", r"system\("]:
            if re.search(p, body, re.I):
                hints.append(p)
        return {"target": target, "status": r.status_code, "hints": hints}
    except Exception as e:
        return {"target": target, "error": str(e)}
