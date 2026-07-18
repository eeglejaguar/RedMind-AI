id="RM-MOD-024"
name="SSRF Surface Detector (parameter listing only)"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        params = re.findall(r"[?&]([A-Za-z0-9_%-]+)=", target.split("?",1)[-1]) if "?" in target else []
        suspect = []
        for name in ["url","redirect","fetch","next","image","callback","download"]:
            if re.search(r"[\?&]" + name + r"=", r.text or "", re.I):
                suspect.append(name)
        return {"target": target, "status_code": r.status_code, "url_params": params, "suspect_param_names": suspect}
    except Exception as e:
        return {"target": target, "error": str(e)}
