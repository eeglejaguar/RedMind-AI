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
