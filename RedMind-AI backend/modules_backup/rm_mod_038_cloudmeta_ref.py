id="RM-MOD-038"
name="Cloud metadata / internal endpoint references"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        refs = []
        for p in ["169.254.169.254","metadata.google","meta-data","instance-data"]:
            if p in body:
                refs.append(p)
        return {"target": target, "status": r.status_code, "refs": refs}
    except Exception as e:
        return {"target": target, "error": str(e)}
