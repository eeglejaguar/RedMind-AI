id="RM-MOD-026"
name="Error & Stacktrace Leakage"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = (r.text or "")[:4000]
        errors = []
        for p in [r"Traceback \(most recent call last\)", r"Exception:", r"SQL syntax", r"Stack trace", r"at com\."]:
            if re.search(p, body, re.I):
                errors.append(p)
        return {"target": target, "status_code": r.status_code, "errors_found": errors, "snippet": body[:600]}
    except Exception as e:
        return {"target": target, "error": str(e)}
