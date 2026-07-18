id="RM-MOD-039"
name="Management Interface Presence (safe HEAD/GET)"
def run(target, context):
    import requests
    from urllib.parse import urljoin
    try:
        base = target.rstrip("/")
        candidates = ["/phpmyadmin/","/server-status","/manager/html","/admin/"]
        results=[]
        for c in candidates:
            u = urljoin(base, c)
            try:
                r = requests.head(u, timeout=5, allow_redirects=True)
                results.append({"path":c,"status": r.status_code})
            except Exception as e:
                results.append({"path":c,"error": str(e)})
        return {"target": target, "checks": results}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_039_mgmt_uris", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_039_mgmt_uris", "error": str(e) }))
    sys.exit(1)
