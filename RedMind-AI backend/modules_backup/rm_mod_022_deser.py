id="RM-MOD-022"
name="Insecure Deserialization Indicators"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        indicators = []
        patterns = [r"\bO:\d+:", r"\bpickle", r"\b__reduce__", r"\bjava\.lang"]
        for p in patterns:
            if re.search(p, body, re.I):
                indicators.append(p)
        return {"target": target, "status_code": r.status_code, "indicators": indicators}
    except Exception as e:
        return {"target": target, "error": str(e)}
