#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    candidates=["/admin/","/backup/","/old/","/config.php","/admin.php","/secret/","/secured/"]
    s=requests.Session(); s.headers["User-Agent"]="RedMind-Paths/1.0"
    findings=[]
    for c in candidates:
        try:
            r=s.get(urljoin(target,c), timeout=8)
            if r.status_code==200 and len(r.text or "")>50:
                findings.append({"path":c,"status":r.status_code,"len":len(r.text or "")})
        except Exception as e:
            pass
    return {"module":"rm_mod_010_paths","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_010_paths","error":str(e)})); sys.exit(1)
