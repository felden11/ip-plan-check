"""Open a GitHub issue with the checker's report."""
import json
import os
import sys
from urllib import error, request

report_file = sys.argv[1] if len(sys.argv) > 1 else "report.txt"
report = open(report_file, encoding="utf-8").read()
repo = os.environ["GITHUB_REPOSITORY"]  # "owner/repo"
token = os.environ["GITHUB_TOKEN"]
payload = {
    "title": "IP plan check failed",
    "body": "The address plan check found problems:\n\n" + report,
}
req = request.Request(
    f"https://api.github.com/repos/{repo}/issues",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "ip-plan-check",
    },
    method="POST",
)

try:
    with request.urlopen(req) as resp:
        issue = json.loads(resp.read().decode("utf-8"))
except error.HTTPError as exc:
    details = exc.read().decode("utf-8", errors="replace")
    raise RuntimeError(f"GitHub issue creation failed: {exc.code} {details}") from exc

print("Opened issue", issue["html_url"])