# rm_mod_015_exposed_files.py
id = "RM-MOD-015"
name = "Exposed Files Detector (fixed)"

def scan_target(target):
    import requests
    from urllib.parse import urljoin
    candidates = [
        "/.env", "/.git/config", "/.git/HEAD", "/.htaccess",
        "/backup.zip","/backup.tar.gz","/db.sql","/wp-config.php.bak",
        "/config.php.bak","/site.bak","/id_rsa","/id_rsa.pub",
        "/credentials.json","/composer.lock","/package.json","/web.config"
    ]

    findings = []
    tokens = ["gitdir:", "private_key", "db_password", "wp_", "define(", "DB_PASSWORD", "AWS_SECRET_ACCESS_KEY"]

    for p in candidates:
        entry = {"path": p, "checked_url": None, "status": None, "snippet": None, "issues": []}
        try:
            u = urljoin(target.rstrip('/') + '/', p.lstrip('/'))
            entry["checked_url"] = u
            # Do HEAD first
            h = requests.head(u, timeout=6, allow_redirects=True)
            entry["status"] = h.status_code
            # If HEAD suggests presence (200) fetch small portion
            if h.status_code == 200:
                r = requests.get(u, timeout=8, stream=True)
                content = r.content[:1600]
                s = content.decode("utf-8", errors="replace")
                entry["snippet"] = s[:800]
                lower = s.lower()
                for t in tokens:
                    if t.lower() in lower:
                        entry["issues"].append(t)
            # If HEAD returns 403, note it but do not try to brute force
            elif h.status_code == 403:
                entry["snippet"] = ""
            findings.append(entry)
        except Exception as e:
            entry["error"] = str(e)
            findings.append(entry)

    return {"target": target, "checks": findings, "total_checked": len(candidates)}

def run(target, context):
    try:
        return scan_target(target)
    except Exception as e:
        return {"target": target, "error": str(e)}

# CLI support so you can run module directly
if __name__ == "__main__":
    import sys, json
    targ = None
    # accept either --target arg or first positional
    if "--target" in sys.argv:
        try:
            targ = sys.argv[sys.argv.index("--target")+1]
        except:
            targ = None
    elif len(sys.argv) > 1:
        targ = sys.argv[1]
    if not targ:
        print(json.dumps({"error":"no target provided"}, indent=2))
        sys.exit(1)
    out = run(targ, {})
    print(json.dumps(out, indent=2))
