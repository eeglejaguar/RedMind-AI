import json
import argparse
import importlib
import time
import sys

# -----------------------------
# Arguments
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True)
parser.add_argument("--checks", required=True)
args = parser.parse_args()

# -----------------------------
# Load checks
# -----------------------------
with open(args.checks, "r") as f:
    checks = json.load(f)

total_checks = len([c for c in checks if c.get("enabled", True)])
completed = 0
results = []

summary = {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "info": 0,
    "total_vulns": 0
}

print(f"\n[+] Target       : {args.target}")
print(f"[+] Total Attacks: {total_checks}")
print("[+] Scan Started...\n")

scan_start = time.time()

# -----------------------------
# Progress Bar Function
# -----------------------------
def show_progress(done, total):
    percent = int((done / total) * 100)
    bar = "#" * (percent // 2) + "-" * (50 - percent // 2)
    # sys.stdout.write(f"\r[{bar}] {percent}% ({done}/{total})")
    sys.stdout.flush()

# -----------------------------
# Execute Attacks█
# -----------------------------
for chk in checks:
    if not chk.get("enabled", True):
        continue

    attack_id = chk["id"]
    
    print(f"CHECK:{attack_id}", flush=True)

    timeout = chk.get("timeout", 5)
    dangerous = chk.get("dangerous", False)

    try:
        mod = importlib.import_module(f"modules.{attack_id}")

        start = time.time()
        out = mod.run(
            target=args.target,
            timeout=timeout,
            dangerous=dangerous
        )
        elapsed = round(time.time() - start, 2)

        # ----------------------------------------
        # Count severity-based vulnerabilities
        # ----------------------------------------
        sev = out.get("severity", "").lower()
        findings = out.get("findings", [])

        count = len(findings)
        summary["total_vulns"] += count

        if sev in summary:
            summary[sev] += count

        results.append({
            "id": attack_id,
            "status": "executed",
            "elapsed": elapsed,
            "output": out
        })

    except Exception as e:
        results.append({
            "id": attack_id,
            "status": "error",
            "error": str(e)
        })

    completed += 1
    print(f"PROGRESS:{completed}/{total_checks}", flush=True)
    # show_progress(completed, total_checks)

# -----------------------------
# Finish
# -----------------------------
total_time = round(time.time() - scan_start, 2)
print("\n\n[+] Scan Completed")
print(f"[+] Total Time: {total_time} seconds\n")

final_output = {
    "results": results,
    "summary": summary,
    "target": args.target,
    "total_time": total_time
}

print(json.dumps(final_output, indent=2))
