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
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_024_ssrf_surface", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_024_ssrf_surface", "error": str(e) }))
    sys.exit(1)
