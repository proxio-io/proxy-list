#!/usr/bin/env python3
"""Mirror the proxio.io free proxy list into this repo.

Runs in GitHub Actions every 20 minutes (see .github/workflows/update.yml).
Stdlib only. Uses the keyless /download endpoint (no API key involved, so
nothing secret lives in the repo). Writes:

  http.txt  https.txt  socks4.txt  socks5.txt   ip:port per line
  all.txt                                       every live proxy, ip:port
  all.json                                      full objects + metadata
  README.md                                     counts table refreshed in place
"""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("PROXIO_BASE", "https://proxio.io")
UA = "proxio-list-mirror/1.0 (+https://github.com/proxio-io/proxy-list)"
PROTOS = ("http", "https", "socks4", "socks5")
LIMIT = 20000  # server cap: settings.PROXIO_DOWNLOAD_MAX
HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(params, retries=4):
    url = f"{BASE}/download?format=json&limit={LIMIT}" + (f"&{params}" if params else "")
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["proxies"]
        except Exception as e:  # network blip / 5xx — back off and retry
            last = e
            time.sleep(5 * (i + 1))
    raise SystemExit(f"fetch failed for {url}: {last}")


def write(name, body):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def main():
    now = datetime.now(timezone.utc).replace(microsecond=0)
    counts = {}
    for proto in PROTOS:
        rows = fetch(f"type={proto}")
        time.sleep(1)  # be polite: one request per second
        write(f"{proto}.txt", "\n".join(f"{r['ip']}:{r['port']}" for r in rows) + "\n")
        counts[proto] = len(rows)

    everything = fetch("")
    write("all.txt", "\n".join(f"{r['ip']}:{r['port']}" for r in everything) + "\n")
    write("all.json", json.dumps({
        "source": BASE, "updated_at": now.isoformat(), "count": len(everything),
        "license": "CC BY 4.0 — attribute proxio.io", "proxies": everything,
    }, indent=None, separators=(",", ":")) + "\n")
    counts["all"] = len(everything)

    # refresh the stats block in README between the markers
    readme_path = os.path.join(HERE, "README.md")
    with open(readme_path, encoding="utf-8") as f:
        readme = f.read()
    start, end = "<!-- stats:start -->", "<!-- stats:end -->"
    if start in readme and end in readme:
        table = [f"Last update: **{now:%Y-%m-%d %H:%M} UTC**", "",
                 "| file | live proxies |", "|---|---:|"]
        for proto in PROTOS:
            table.append(f"| [`{proto}.txt`]({proto}.txt) | {counts[proto]:,} |")
        table.append(f"| [`all.txt`](all.txt) / [`all.json`](all.json) | {counts['all']:,} |")
        head, rest = readme.split(start, 1)
        _, tail = rest.split(end, 1)
        readme = head + start + "\n" + "\n".join(table) + "\n" + end + tail
        write("README.md", readme)

    print(json.dumps(counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
