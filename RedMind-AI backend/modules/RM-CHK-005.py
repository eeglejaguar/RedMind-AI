import requests
from finding_template import create_finding


def run(target, timeout=15, dangerous=False):

    results = []

    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    endpoints = [
        "/setup",
        "/admin/setup",
        "/install",
        "/initialize",
        "/api/setup"
    ]


    for ep in endpoints:

        try:

            url = target.rstrip("/") + ep


            r = requests.get(
                url,
                headers=headers,
                timeout=timeout
            )


            if r.status_code == 200:


                results.append(

                    create_finding(

                        issue=
                        "Unauthorized Setup Resource Exposure",


                        parameter=
                        "Endpoint Path",


                        payload=
                        ep,


                        url=
                        url,


                        evidence=
                        r.text[:300],


                        confidence=
                        "HIGH",


                        description=
                        "A setup-related resource is accessible without authentication. Public exposure of setup resources may disclose sensitive configuration information or administrative functionality.",


                        remediation=
                        "Remove setup resources from production deployments, enforce authentication, and restrict access to administrative endpoints.",


                        references=[
                            "OWASP Security Misconfiguration",
                            "CWE-16: Configuration"
                        ]

                    )

                )


        except Exception:
            pass



    return {

        "check_id":
        "RM-CHK-005",


        "severity":
        "CRITICAL",


        "target":
        target,


        "dangerous":
        dangerous,


        "findings":
        results,


        "summary": {

            "tested_requests":
            len(endpoints),


            "positive_hits":
            len(results)

        }

    }