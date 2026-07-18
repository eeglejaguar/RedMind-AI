# =====================================================
# RedMind-AI – VAPT Configuration
# Optimized for Speed + Real Attacks
# =====================================================

MODE = "DEMO"   # DEMO (fast) | FULL (complete)

VAPT_CHECKS = []

for i in range(1, 180):

    # -------------------------
    # DEMO MODE (FAST)
    # -------------------------
    if MODE == "DEMO":
        enabled = True if i <= 40 else False   # only 40 attacks
        timeout = 5 if i <= 20 else 3          # fast timeout

    # -------------------------
    # FULL MODE (REAL SCAN)
    # -------------------------
    else:
        enabled = True

        if 1 <= i <= 20:          # SQLi
            timeout = 15
        elif 21 <= i <= 40:       # XSS
            timeout = 8
        elif 41 <= i <= 80:       # Auth / IDOR
            timeout = 10
        elif 81 <= i <= 120:      # SSRF / RCE
            timeout = 20
        else:                     # Logic / Config
            timeout = 10

    dangerous = True if i <= 120 else False

    VAPT_CHECKS.append({
        "id": f"RM-CHK-{i:03d}",
        "enabled": enabled,
        "timeout": timeout,
        "dangerous": dangerous
    })
