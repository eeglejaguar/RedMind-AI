# RM-MOD-013 - HSTS missing check
id = "RM-MOD-013"
name = "HSTS Missing Check"
description = "Detect missing or weak Strict-Transport-Security header."

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8, allow_redirects=True)
        hsts = r.headers.get("strict-transport-security")
        result = {"has_hsts": bool(hsts)}
        if hsts:
            result["hsts_value"] = hsts
        return {"target": target, "status_code": r.status_code, "hsts": result}
    except Exception as e:
        return {"target": target, "error": str(e)}
