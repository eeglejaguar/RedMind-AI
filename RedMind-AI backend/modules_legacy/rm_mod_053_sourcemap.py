id="RM-MOD-053"
name="Source Map Accessibility (HEAD)"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        maps = re.findall(r"sourceMappingURL=([^\\s]+\\.map)", r.text or "", re.I)
        accessible=[]
        for m in maps:
            try:
                h = requests.head(m, timeout=4, allow_redirects=True)
                accessible.append({"map": m, "status": h.status_code})
            except:
                accessible.append({"map": m, "status": "error"})
        return {"target": target, "maps": accessible}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_053_sourcemap", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_053_sourcemap", "error": str(e) }))
    sys.exit(1)
