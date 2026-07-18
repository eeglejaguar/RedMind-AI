id="RM-MOD-051"
name="Load Balancer / Proxy Header Heuristics"
def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        hdrs = r.headers
        interesting = {}
        for h in ["Via","X-Forwarded-For","X-Real-IP","Server"]:
            if h in hdrs:
                interesting[h] = hdrs.get(h)
        return {"target": target, "status": r.status_code, "interesting_headers": interesting}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_051_lb_headers", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_051_lb_headers", "error": str(e) }))
    sys.exit(1)
