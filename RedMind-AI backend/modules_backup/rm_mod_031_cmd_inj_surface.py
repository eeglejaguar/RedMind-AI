id="RM-MOD-031"
name="Command-Injection Parameter Heuristics"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        suspects = [n for n in ["cmd","command","execute","shell","run"] if re.search(r"[?&]"+n+r"=", target) or re.search(r"name=[\"\\\']?"+n, body, re.I)]
        return {"target": target, "status_code": r.status_code, "suspect_params": suspects}
    except Exception as e:
        return {"target": target, "error": str(e)}
