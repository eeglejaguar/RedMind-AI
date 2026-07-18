#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    s=requests.Session(); s.headers["User-Agent"]="RedMind-CookieCheck/1.0"
    findings=[]
    try:
        r=s.get(urljoin(target,"/"), timeout=8)
        # look for Set-Cookie headers (requests merges multiple cookies)
        raw = r.headers.get("Set-Cookie","")
        if raw:
            # simple checks
            if "HttpOnly" not in raw or "Secure" not in raw:
                findings.append({"set_cookie":raw})
    except Exception as e:
        findings.append({"error":str(e)})
    return {"module":"rm_mod_008_cookies","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_008_cookies","error":str(e)})); sys.exit(1)
