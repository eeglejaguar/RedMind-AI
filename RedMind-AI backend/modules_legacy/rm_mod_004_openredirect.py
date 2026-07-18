#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    url = urljoin(target, "/hpp/params.php")
    session = requests.Session()
    session.headers["User-Agent"]="RedMind-OR-Checker/1.0"
    payload = "http://evil.example.com/"
    findings=[]
    try:
        r = session.get(url, params={"p":payload,"pp":"12"}, timeout=10, allow_redirects=False)
        loc = r.headers.get("Location","")
        if r.status_code in (301,302) and "evil.example.com" in (loc or ""):
            findings.append({"action":url,"location":loc})
        else:
            findings.append({"status":r.status_code,"location":loc})
    except Exception as e:
        findings.append({"error":str(e)})
    return {"module":"rm_mod_004_openredirect","target":target,"vulnerable":any("evil.example.com" in (f.get("location","") or "") for f in findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_004_openredirect","error":str(e)})); sys.exit(1)
