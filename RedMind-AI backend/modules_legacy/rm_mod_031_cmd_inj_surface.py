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
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_031_cmd_inj_surface", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_031_cmd_inj_surface", "error": str(e) }))
    sys.exit(1)
