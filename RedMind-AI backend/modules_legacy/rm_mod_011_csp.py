#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    paths=["/","/product.php","/login.php"]
    s=requests.Session(); s.headers["User-Agent"]="RedMind-CSP/1.0"
    findings=[]
    for p in paths:
        try:
            r=s.get(urljoin(target,p), timeout=8)
            csp=r.headers.get("Content-Security-Policy","")
            if not csp or ("unsafe-inline" in csp) or ("'unsafe-inline'" in csp):
                findings.append({"path":p,"csp":csp})
        except:
            pass
    return {"module":"rm_mod_011_csp","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_011_csp","error":str(e)})); sys.exit(1)
