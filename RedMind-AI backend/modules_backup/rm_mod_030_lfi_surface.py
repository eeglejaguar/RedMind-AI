id="RM-MOD-030"
name="LFI Parameter Surface"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        suspect = []
        for name in ["file","page","template","view","path"]:
            if re.search(r"[?&]"+name+r"=", target) or re.search(r"name=[\"\\\']?"+name, body, re.I):
                suspect.append(name)
        return {"target": target, "status_code": r.status_code, "suspect_params": suspect}
    except Exception as e:
        return {"target": target, "error": str(e)}
