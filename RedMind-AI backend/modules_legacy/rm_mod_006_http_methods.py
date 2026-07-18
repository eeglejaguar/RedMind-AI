#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    paths=["/","/product.php"]
    methods=["OPTIONS","TRACE","PUT","DELETE"]
    s=requests.Session(); s.headers["User-Agent"]="RedMind-HTTPMethods/1.0"
    findings=[]
    for p in paths:
        for m in methods:
            try:
                r=s.request(m, urljoin(target,p), timeout=8, allow_redirects=False)
                if m in ("PUT","DELETE") and r.status_code in (200,201,204):
                    findings.append({"path":p,"method":m,"status":r.status_code})
                if m=="TRACE" and r.status_code==200 and "TRACE" in (r.text or ""):
                    findings.append({"path":p,"method":m,"status":r.status_code})
            except Exception as e:
                pass
    return {"module":"rm_mod_006_http_methods","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_006_http_methods","error":str(e)})); sys.exit(1)
