# =====================================================
# RedMind AI - Attack Knowledge Base
# Used for Reporting, CVSS, Mitigation & Viva
# =====================================================

ATTACK_KNOWLEDGE = {

    # =========================
    # SQL INJECTION
    # =========================
    "RM-CHK-001": {
        "cvss_guess": 9.8,
        "description": "Unsanitized input leads to execution of arbitrary SQL queries",
        "affected_components": ["Login forms", "Search parameters"],
        "cves": [],
        "detection_signatures": ["' OR 1=1", "UNION SELECT", "SLEEP("],
        "mitigation": "Use parameterized queries and input validation",
        "references": ["OWASP A03:2021"],
        "notes": "Most common web vulnerability"
    },

    "RM-CHK-003": {
        "cvss_guess": 9.1,
        "description": "Database response delay indicates time-based SQL injection",
        "affected_components": ["API query parameters"],
        "cves": [],
        "detection_signatures": ["SLEEP", "WAITFOR DELAY"],
        "mitigation": "Prepared statements and DB timeout restrictions",
        "references": ["OWASP SQLi"],
        "notes": "Blind exploitation technique"
    },

    # =========================
    # XSS
    # =========================
    "RM-CHK-016": {
        "cvss_guess": 7.4,
        "description": "User input reflected without sanitization enabling script execution",
        "affected_components": ["Search fields", "Error messages"],
        "cves": [],
        "detection_signatures": ["<script>", "onerror=", "alert("],
        "mitigation": "Output encoding and Content Security Policy",
        "references": ["OWASP A07:2021"],
        "notes": "Client-side execution"
    },

    "RM-CHK-017": {
        "cvss_guess": 8.8,
        "description": "Persistent malicious scripts stored in backend database",
        "affected_components": ["Comment sections", "User profiles"],
        "cves": [],
        "detection_signatures": ["<script>", "<img src=x onerror="],
        "mitigation": "Input sanitization and HTML encoding",
        "references": ["OWASP Stored XSS"],
        "notes": "High impact due to persistence"
    },

    # =========================
    # AUTHENTICATION
    # =========================
    "RM-CHK-031": {
        "cvss_guess": 9.6,
        "description": "Improper authentication mechanisms allow account takeover",
        "affected_components": ["Login APIs"],
        "cves": [],
        "detection_signatures": ["200 OK after invalid login"],
        "mitigation": "Strong authentication controls and MFA",
        "references": ["OWASP A02:2021"],
        "notes": "Critical identity risk"
    },

    # =========================
    # IDOR / ACCESS CONTROL
    # =========================
    "RM-CHK-056": {
        "cvss_guess": 8.9,
        "description": "Unauthorized access to objects by manipulating identifiers",
        "affected_components": ["REST APIs"],
        "cves": [],
        "detection_signatures": ["user_id=", "account_id="],
        "mitigation": "Server-side authorization checks",
        "references": ["OWASP API1:2019"],
        "notes": "Most common API flaw"
    },

    # =========================
    # SSRF
    # =========================
    "RM-CHK-076": {
        "cvss_guess": 9.4,
        "description": "Server fetches attacker-controlled internal resources",
        "affected_components": ["URL fetch endpoints"],
        "cves": [],
        "detection_signatures": ["169.254.169.254", "localhost"],
        "mitigation": "URL allowlisting and network isolation",
        "references": ["OWASP SSRF"],
        "notes": "Cloud metadata risk"
    },

    # =========================
    # RCE
    # =========================
    "RM-CHK-086": {
        "cvss_guess": 9.9,
        "description": "User input executed as system command",
        "affected_components": ["OS command handlers"],
        "cves": [],
        "detection_signatures": [";id", "|whoami"],
        "mitigation": "Avoid OS calls, strict input validation",
        "references": ["OWASP A03:2021"],
        "notes": "Full system compromise"
    },

    # =========================
    # BUSINESS LOGIC
    # =========================
    "RM-CHK-115": {
        "cvss_guess": 8.2,
        "description": "Application workflow abused without breaking authentication",
        "affected_components": ["Payment systems"],
        "cves": [],
        "detection_signatures": ["Repeated discount usage"],
        "mitigation": "Server-side logic validation",
        "references": ["OWASP Business Logic"],
        "notes": "Hard to detect automatically"
    },

    # =========================
    # DEPLOYMENT / MISCONFIG
    # =========================
    "RM-CHK-179": {
        "cvss_guess": 9.8,
        "description": "Initial setup endpoints remain exposed in production",
        "affected_components": ["Admin setup APIs"],
        "cves": [],
        "detection_signatures": ["setup.*admin.*200"],
        "mitigation": "Disable bootstrap endpoints after installation",
        "references": ["CIS Benchmarks"],
        "notes": "Secure Deployment Practices"
    }

}
