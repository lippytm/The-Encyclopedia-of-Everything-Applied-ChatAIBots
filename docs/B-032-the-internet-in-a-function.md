# B-032: The Internet in a Function

### requests, APIs, JSON Responses, and the HTTP Client Every Developer Needs

> *"Every service on the internet speaks HTTP. When you learn to make HTTP requests from Python, you gain the ability to talk to GitHub, OpenAI, weather services, blockchain APIs, and thousands of other systems — all with the same five lines of code."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Make GET, POST, PUT, and DELETE HTTP requests with `requests`
2. Parse JSON API responses into Python dicts
3. Handle HTTP errors (4xx, 5xx) and network failures gracefully
4. Use request headers, query parameters, and authentication tokens
5. Build an `api-client.py` that fetches live data from a public API with full error handling

**Prerequisite:** B-026 through B-031

**Build Artifact:** `~/developer-workspace/projects/python-foundations/api_client.py`

**Credential:** `CCSLL-L1-B032-APIEngineer` — on-chain on Base

---

## Chapter 1: Installing requests

```bash
# Install (in your virtual environment — see B-035)
pip install requests

# Or with pip3
pip3 install requests

# Verify
python3 -c "import requests; print(requests.__version__)"
```

---

## Chapter 2: GET Requests — Fetching Data

```python
import requests

# Basic GET request
response = requests.get("https://httpbin.org/get")

# The response object
print(response.status_code)    # 200
print(response.headers)        # dict of response headers
print(response.text)           # raw text body
print(response.json())         # parsed JSON (dict)

# Check for success
if response.status_code == 200:
    data = response.json()
    print("Success:", data)

# Shorthand: raise_for_status() raises HTTPError on 4xx/5xx
response.raise_for_status()    # silent on 200, raises on errors
```

---

## Chapter 3: Query Parameters and Headers

```python
import requests

# Query parameters — appended to URL as ?key=value&key2=value2
params = {
    "q":      "python tutorial",
    "limit":  5,
    "format": "json",
}
response = requests.get("https://httpbin.org/get", params=params)
print(response.url)    # shows full URL with params

# Headers — authentication, content type, etc.
headers = {
    "User-Agent":    "lippytmai/1.0",
    "Accept":        "application/json",
    "Authorization": "******",
}
response = requests.get("https://httpbin.org/headers", headers=headers)
print(response.json())
```

---

## Chapter 4: POST, PUT, DELETE

```python
import requests

# POST — send data (create a resource)
payload = {"name": "lippytmai", "role": "teacher", "level": 5}
response = requests.post(
    "https://httpbin.org/post",
    json=payload,          # auto-sets Content-Type: application/json
)
print(response.status_code)    # 200
print(response.json()["json"]) # echoes back your payload

# POST with form data (not JSON)
response = requests.post(
    "https://httpbin.org/post",
    data={"field": "value"},   # form-encoded
)

# PUT — update a resource
response = requests.put(
    "https://httpbin.org/put",
    json={"status": "updated"},
)

# DELETE — remove a resource
response = requests.delete("https://httpbin.org/delete")
print(response.status_code)
```

---

## Chapter 5: Error Handling for HTTP

```python
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException,
)

def safe_get(url: str, timeout: int = 10) -> dict:
    """Make a GET request with full error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()    # raises HTTPError for 4xx/5xx
        return response.json()
    except Timeout:
        print(f"[error] Request timed out after {timeout}s: {url}")
    except ConnectionError:
        print(f"[error] Cannot connect to: {url}")
    except HTTPError as e:
        status = e.response.status_code
        if status == 404:
            print(f"[error] Not found (404): {url}")
        elif status == 401:
            print("[error] Unauthorized — check your API token")
        elif status == 429:
            print("[error] Rate limited — slow down requests")
        elif status >= 500:
            print(f"[error] Server error ({status}): {url}")
        else:
            print(f"[error] HTTP {status}: {url}")
    except RequestException as e:
        print(f"[error] Unexpected request error: {e}")
    return {}
```

---

## Chapter 6: The Build — API Client

```python
#!/usr/bin/env python3
"""
api_client.py — B-032 Build Artifact

A reusable HTTP API client demonstrating:
- GET with query parameters
- JSON response parsing
- Full error handling
- Public API integration (Open-Meteo weather — no API key needed)
"""
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException
from typing import Any, Optional


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather code descriptions
WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers",
    95: "Thunderstorm", 99: "Thunderstorm with heavy hail",
}


class APIClient:
    """Generic HTTP API client with error handling."""

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "lippytmai-api-client/1.0"})

    def get(self, path: str = "", params: Optional[dict] = None) -> Optional[dict]:
        """GET request with full error handling."""
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Timeout:
            print(f"[timeout] {url} — no response in {self.timeout}s")
        except ConnectionError:
            print(f"[connection error] Cannot reach {url}")
        except HTTPError as e:
            print(f"[http error] {e.response.status_code}: {url}")
        except RequestException as e:
            print(f"[request error] {e}")
        return None


def get_weather(latitude: float, longitude: float) -> None:
    """Fetch and display current weather for a location."""
    client = APIClient(OPEN_METEO_URL)
    params = {
        "latitude":       latitude,
        "longitude":      longitude,
        "current":        "temperature_2m,weathercode,windspeed_10m",
        "temperature_unit": "celsius",
        "windspeed_unit": "kmh",
        "timezone":       "auto",
    }

    print(f"Fetching weather for ({latitude}, {longitude})...")
    data = client.get(params=params)

    if not data:
        print("Could not retrieve weather data.")
        return

    current = data.get("current", {})
    temp    = current.get("temperature_2m", "N/A")
    wind    = current.get("windspeed_10m", "N/A")
    code    = current.get("weathercode", -1)
    desc    = WMO_CODES.get(code, f"Unknown (code {code})")
    tz      = data.get("timezone", "unknown")

    print(f"""
╔══════════════════════════════════════╗
║         Current Weather              ║
║                                      ║
║  Location: {latitude}°N, {longitude}°E
║  Timezone: {tz}
║  Condition: {desc}
║  Temperature: {temp}°C
║  Wind Speed: {wind} km/h
╚══════════════════════════════════════╝
""")


def main() -> None:
    # San Francisco, CA
    get_weather(latitude=37.7749, longitude=-122.4194)

    # London, UK
    get_weather(latitude=51.5074, longitude=-0.1278)


if __name__ == "__main__":
    main()
```

```bash
pip3 install requests
python3 ~/developer-workspace/projects/python-foundations/api_client.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-032 Verification ==="
python3 -c "
import requests
r = requests.get('https://httpbin.org/json', timeout=10)
r.raise_for_status()
data = r.json()
print('✅ GET request successful, status:', r.status_code)
print('✅ JSON keys:', list(data.keys()))
"
python3 ~/developer-workspace/projects/python-foundations/api_client.py
```

---

## Further Reading

- 📄 [`docs/B-031-errors-that-tell-the-truth.md`](B-031-errors-that-tell-the-truth.md) — Exception patterns used here
- 📄 [`docs/B-029-dictionaries-the-data-swiss-army-knife.md`](B-029-dictionaries-the-data-swiss-army-knife.md) — JSON parsing with dicts
- 📄 [`docs/ai-trading-bots-intelligence.md`](ai-trading-bots-intelligence.md) — APIs in the trading bot context
- 🏠 [`README.md`](../README.md) — Encyclopedia home
