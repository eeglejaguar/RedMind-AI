#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    s=requests.Session(); s.headers["User-Agent"]="RedMind-Banner/1.0"
    findings=[]
    try:
        r=s.get(target, timeout=8)
        server=r.headers.get("Server","")
        xpb=r.headers.get("X-Powered-By","")
        if server and any(ch.isdigit() for ch in server):
            findings.append({"Server":server})
        if xpb and any(ch.isdigit() for ch in xpb):
            findings.append({"X-Powered-By":xpb})
    except Exception as e:
        findings.append({"error":str(e)})
    return {"module":"rm_mod_009_server_banner","target":target,"vulnerable":bool(findings),"findings":findings}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_009_server_banner","error":str(e)})); sys.exit(1)
