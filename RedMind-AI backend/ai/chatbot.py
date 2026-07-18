from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_remediation(vulnerability):


    prompt = f"""

You are REDMIND-AI automated remediation engine.


Analyze this vulnerability:

Issue:
{vulnerability.get("issue")}


Severity:
{vulnerability.get("severity")}


Evidence:
{vulnerability.get("evidence")}


Payload:
{vulnerability.get("payload")}


Provide professional remediation.

Return ONLY this format:


ROOT CAUSE:
Explain why this happens.


IMPACT:
Explain the security impact.


REMEDIATION:
Give practical fixes.


SECURE IMPLEMENTATION:
Provide secure coding/configuration examples.


PREVENTION:
Give prevention steps.


"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":
                "You are REDMIND-AI remediation engine."
            },


            {
                "role":"user",
                "content":prompt
            }

        ],

        temperature=0.2

    )


    return response.choices[0].message.content

def ask_ai(message, vulnerability=None):


    context = ""


    if vulnerability:

        context = f"""

Vulnerability Details:

Issue:
{vulnerability.get('issue')}


Severity:
{vulnerability.get('severity')}


Evidence:
{vulnerability.get('evidence')}


Target:
{vulnerability.get('target')}


"""

    prompt=f"""

    User Question:

    {message}


    Provide a professional cybersecurity response suitable for a VAPT report.

    """

    SYSTEM_CONTEXT = """

    You are REDMIND-AI, an advanced AI cybersecurity assistant integrated into a VAPT platform.

    Your responsibilities:

    1. Explain vulnerabilities detected by REDMIND-AI.
    2. Provide professional remediation advice.
    3. Explain security concepts.
    4. Answer questions about VAPT attacks and security testing.
    5. Help developers fix vulnerabilities.

    REDMIND-AI performs these security assessments:

    Vulnerability Categories:

    1. SQL Injection
    - Error Based SQL Injection
    - Boolean Based SQL Injection
    - Time Based SQL Injection
    - Union SQL Injection
    - Authentication Bypass SQL Injection


    2. Cross Site Scripting (XSS)
    - Reflected XSS
    - Stored XSS
    - DOM XSS


    3. Authentication Testing
    - Weak Password Detection
    - Brute Force Protection
    - Session Management
    - Cookie Security
    - MFA Issues


    4. Access Control
    - IDOR
    - Privilege Escalation
    - Unauthorized Access


    5. Server Side Security
    - SSRF
    - File Inclusion
    - Remote Code Execution
    - Path Traversal


    6. API Security
    - Broken Authentication
    - Excessive Data Exposure
    - Rate Limit Issues
    - Security Misconfiguration


    7. Deployment Security
    - Exposed Services
    - Security Headers
    - Information Disclosure
    - Directory Listing


    When explaining vulnerabilities always use this structure:


    Summary:
    Short explanation of the vulnerability.


    Risk Level:
    LOW / MEDIUM / HIGH / CRITICAL


    Impact:
    Explain what an attacker could achieve.


    Root Cause:
    Explain why the vulnerability happens.


    Remediation:
    Provide practical fixes.


    Secure Implementation:
    Provide coding/configuration recommendations.


    Prevention:
    Explain how to avoid it in future.


    Rules:

    - Do not provide attack instructions for harming systems.
    - Focus on defensive security, testing, and remediation.
    - Answer as a professional penetration testing assistant.
    - Keep answers concise but detailed.
    - Use bullet points instead of long paragraphs.

    """


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",


        messages=[

            {
            "role":"system",
            "content":SYSTEM_CONTEXT
            },


            {
            "role":"user",
            "content":prompt
            }

        ],


        temperature=0.2

    )



    return response.choices[0].message.content