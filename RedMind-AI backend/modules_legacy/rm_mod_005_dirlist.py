#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    candidates = ["/","/admin/","/backup/","/old/"]
    findings=[]
    s=requests.Session(); s.headers["User-Agent"]="RedMind-Dirlist/1.0"
    for c in candidates:
        try:
            r=s.get(urljoin(target,c), timeout=8)
            body=(r.text or "").lower()
            if "index of /" in body or "directory listing for" in body:
                findings.append({"path":c,"status":r.status_code})
        except Exception as e:
            findings.append({"path":c,"error":str(e)})
    return {"module":"rm_mod_005_dirlist","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        import argparse
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_005_dirlist","error":str(e)})); sys.exit(1)
