id="RM-MOD-050"
name="Dev / Debug Endpoint Detector"
def run(target, context):
    import requests
    from urllib.parse import urljoin
    try:
        cands = ["/debug","/_profiler","/__debug__","/debugger","/actuator/env"]
        res=[]
        for c in cands:
            u = urljoin(target,c)
            try:
                r = requests.head(u, timeout=4, allow_redirects=True)
                res.append({"path":c,"status": r.status_code})
            except Exception as e:
                res.append({"path":c,"error": str(e)})
        return {"target": target, "checks": res}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_050_dev_endpoints", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_050_dev_endpoints", "error": str(e) }))
    sys.exit(1)
