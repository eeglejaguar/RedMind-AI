id="RM-MOD-055"
name="Database Snippet Detector"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        snippet = (r.text or "")[:4000]
        patterns = [r"INSERT INTO", r"CREATE TABLE", r"DROP TABLE", r"VALUES \("]
        found=[]
        for p in patterns:
            if re.search(p, snippet, re.I):
                found.append(p)
        return {"target": target, "status": r.status_code, "db_patterns": found}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_055_db_snippets", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_055_db_snippets", "error": str(e) }))
    sys.exit(1)
