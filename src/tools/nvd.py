import re
import requests


NVD_API_URL = (
    "https://services.nvd.nist.gov/rest/json/cves/2.0"
)


def extract_cve_id(text):
    """Extract a CVE identifier from user text."""

    if not isinstance(text, str):
        return None

    match = re.search(
        r"\bCVE-\d{4}-\d{4,}\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(0).upper()

    return None


def nvd_cve_tool(cve_id, timeout=15):
    """Retrieve CVE information from the public NVD API."""

    if not cve_id:
        return {
            "success": False,
            "error": "CVE ID not found",
        }

    try:
        response = requests.get(
            NVD_API_URL,
            params={"cveId": cve_id},
            timeout=timeout,
        )

        if response.status_code != 200:
            return {
                "success": False,
                "cve_id": cve_id,
                "http_status": response.status_code,
                "error": "NVD API request failed",
            }

        data = response.json()

        vulnerabilities = data.get(
            "vulnerabilities",
            []
        )

        if not vulnerabilities:
            return {
                "success": False,
                "cve_id": cve_id,
                "http_status": response.status_code,
                "error": "CVE not found",
            }

        cve = vulnerabilities[0].get(
            "cve",
            {}
        )

        descriptions = cve.get(
            "descriptions",
            []
        )

        description = ""

        for item in descriptions:
            if item.get("lang") == "en":
                description = item.get(
                    "value",
                    ""
                )
                break

        return {
            "success": True,
            "tool": "NIST NVD CVE API",
            "cve_id": cve.get("id", cve_id),
            "published": cve.get("published"),
            "last_modified": cve.get("lastModified"),
            "description": description,
            "http_status": response.status_code,
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "cve_id": cve_id,
            "error": str(e),
        }
