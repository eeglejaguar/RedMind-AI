id="RM-MOD-043"
name="Reflected Parameters Inventory"
def run(target, context):
    import requests, re
    from urllib.parse import urlparse, parse_qs
    try:
        r = requests.get(target, timeout=8)
        params = []
        q = urlparse(target).query
        if q:
            params = list(parse_qs(q).keys())
        reflected = []
        for p in params:
            if re.search(r"["+p+r"]", r.text or "", re.I):
                reflected.append(p)
        return {"target": target, "status": r.status_code, "params": params, "reflected": reflected}
    except Exception as e:
        return {"target": target, "error": str(e)}
