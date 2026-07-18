#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    candidates=["/showimage.php?file=./pictures/1.jpg","/showimage.php?file=./pictures/2.jpg","/product.php?pic=1","/product.php?pic=2","/signup.php","/cart.php"]
    s=requests.Session(); s.headers["User-Agent"]="RedMind-ExposedFiles/1.0"
    findings=[]
    for c in candidates:
        try:
            r=s.get(urljoin(target,c), timeout=10)
            if r.status_code==200 and len(r.content or b"")>200:
                findings.append({"path":c,"status":r.status_code,"len":len(r.content or b"")})
        except Exception as e:
            findings.append({"path":c,"error":str(e)})
    return {"module":"rm_mod_015_exposed_files","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_015_exposed_files","error":str(e)})); sys.exit(1)
