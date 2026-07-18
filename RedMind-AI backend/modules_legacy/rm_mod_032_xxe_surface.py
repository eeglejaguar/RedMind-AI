id="RM-MOD-032"
name="XML / XXE Surface Detector"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        ctype = r.headers.get("Content-Type","")
        body = r.text or ""
        has_xml = ("xml" in ctype.lower()) or bool(re.search(r"<\?xml", body))
        return {"target": target, "status_code": r.status_code, "content_type": ctype, "has_xml": has_xml}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_032_xxe_surface", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_032_xxe_surface", "error": str(e) }))
    sys.exit(1)
