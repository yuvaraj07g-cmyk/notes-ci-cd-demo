"""Smoke test: is the NEW version live and healthy?

Usage: python scripts/smoke.py https://your-app.onrender.com [--expect-sha SHA]
Retries for up to 5 minutes while the host switches to the new version.
"""
import argparse
import json
import sys
import time
import urllib.request


def get(url: str):
    with urllib.request.urlopen(url, timeout=30) as r:  # noqa: S310
        return r.status, json.loads(r.read())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--expect-sha", default=None)
    args = p.parse_args()
    base = args.url.rstrip("/")

    deadline = time.time() + 300
    while time.time() < deadline:
        try:
            status, body = get(f"{base}/health")
            version = body.get("version")
            print(f"waiting... {status} version={version}")
            if status == 200 and (not args.expect_sha or version == args.expect_sha):
                print(f"ok   /health -> {status}, version {version}")
                status, _ = get(f"{base}/notes")
                print(f"ok   /notes  -> {status}")
                print("Smoke test passed")
                return 0
        except Exception as e:  # app still starting / switching
            print(f"waiting... {e}")
        time.sleep(10)

    print("Smoke test FAILED: new version never became healthy")
    return 1


if __name__ == "__main__":
    sys.exit(main())
