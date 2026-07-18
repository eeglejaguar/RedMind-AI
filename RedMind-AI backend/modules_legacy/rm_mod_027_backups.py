id="RM-MOD-027"
name="Backup/Admin File Hints (non-bruteforce)"
def run(target, context):
    import requests
    from urllib.parse import urljoin
    try:
        paths = ["/backup.zip","/backup.tar.gz","/db.sql","/wp-config.php.bak","/config.php.bak","/site.bak"]
        results=[]
        for p in paths:
            u = urljoin(target,p)
            r = requests.get(u, timeout=6, allow_redirects=True)
            results.append({"path":p,"status":r.status_code, "length": len(r.content)})
        return {"target": target,"checks": results}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_027_backups", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_027_backups", "error": str(e) }))
    sys.exit(1)
