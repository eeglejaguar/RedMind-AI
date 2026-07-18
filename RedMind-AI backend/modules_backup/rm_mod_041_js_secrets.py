id="RM-MOD-041"
name="JS / Source Map Sensitive Strings Scanner"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        finds=[]
        body = r.text or ""
        for m in re.finditer(r"(sourceMappingURL=.*\.map|\\b(secret|token|password|apikey)\\b)", body, re.I):
            finds.append(m.group(0)[:200])
        return {"target": target, "status": r.status_code, "matches": finds[:20]}
    except Exception as e:
        return {"target": target, "error": str(e)}
