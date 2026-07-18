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
                        "Exposed Application Setup Interface",


                        parameter=
                        "URL Path",


                        payload=
                        ep,


                        url=
                        url,


                        evidence=
                        r.text[:300],


                        confidence=
                        "HIGH",


                        description=
                        "An application setup or initialization interface is publicly accessible. Exposed setup pages may reveal configuration details or allow unauthorized administrative actions.",


                        remediation=
                        "Remove setup interfaces from production systems, disable unused installation pages, and restrict administrative routes with authentication.",


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
        "RM-CHK-004",


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