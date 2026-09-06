# Free proxy list — HTTP · HTTPS · SOCKS4 · SOCKS5

Live, re-checked public proxies from **[proxio.io](https://proxio.io)**, mirrored here **every 20 minutes**.
Every entry answered a real protocol check within the last 7 days; dead proxies drop off automatically.

<!-- stats:start -->
Last update: **2026-09-06 13:20 UTC**

| file | live proxies |
|---|---:|
| [`http.txt`](http.txt) | 8,907 |
| [`https.txt`](https.txt) | 7,061 |
| [`socks4.txt`](socks4.txt) | 2,050 |
| [`socks5.txt`](socks5.txt) | 3,882 |
| [`all.txt`](all.txt) / [`all.json`](all.json) | 20,000 |
<!-- stats:end -->

## Files

| file | format |
|---|---|
| `http.txt`, `https.txt`, `socks4.txt`, `socks5.txt` | one `ip:port` per line, newest-checked first |
| `all.txt` | every live proxy, `ip:port` |
| `all.json` | full objects: protocols, country, city, anonymity, latency, reliability score, uptime, check history |

Raw URLs are stable — pin them in scripts:

```bash
curl -s https://raw.githubusercontent.com/proxio-io/proxy-list/main/socks5.txt
```

## Want filters, JSON and a proper API?

The site serves the same data with live filters — by country, protocol, anonymity, SSL, Google-passed:

- Web: **https://proxio.io** · [by country](https://proxio.io/proxy/) · [SOCKS5](https://proxio.io/proxy/socks5/) · [HTTPS](https://proxio.io/proxy/https/)
- Keyless download: `https://proxio.io/download?type=socks5&country=Netherlands&limit=500` (`&format=json` for JSON)
- Free JSON API (free key, 2,000 calls/day): **https://proxio.io/api/**

```python
import requests
r = requests.get("https://proxio.io/api/list",
                 params={"type": "socks5", "anonymity": "Elite", "limit": 50},
                 headers={"X-Key": "YOUR_KEY"})
for p in r.json()["proxies"]:
    print(p["ip"], p["port"], p["country"], p["latency_s"], p["reliability"])
```

Clients: `pip install proxio` · `npm i proxio`

## Fields in `all.json`

| field | meaning |
|---|---|
| `protocols` | every protocol the proxy answered on |
| `anonymity` | `Elite` (hides IP + proxy use) · `Anonymous` (hides IP) · `Transparent` |
| `latency_s` | round-trip of last successful check, seconds |
| `reliability` | 0–100 score from check history (`null` until 3 checks) |
| `uptime` | recency-weighted success rate 0–1 |
| `last_results` | recent outcomes as `1`/`0` string, newest last |
| `last_checked`, `first_seen` | ISO timestamps |

## How it is checked

Each proxy is tested roughly every 5 minutes with a real request through the protocol it claims
(HTTP GET, CONNECT for HTTPS, SOCKS4/5 handshake), measuring latency and anonymity from the
headers the target sees. Results feed a reliability score so you can skip the flaky ones.

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free for any use, please link
back to [proxio.io](https://proxio.io). Public proxies are operated by third parties; use them responsibly
and never send credentials through a proxy you don't trust.
