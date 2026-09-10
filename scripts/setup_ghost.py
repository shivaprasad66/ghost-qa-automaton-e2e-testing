import json
import os
import sys
import time
import urllib.error
import urllib.request


GHOST_URL = os.getenv("GHOST_URL", "http://localhost:3001").rstrip("/")
GHOST_EMAIL = os.getenv("GHOST_EMAIL")
GHOST_PASSWORD = os.getenv("GHOST_PASSWORD")

READY_URL = f"{GHOST_URL}/ghost/api/admin/site/"
SETUP_URL = f"{GHOST_URL}/ghost/api/admin/authentication/setup/"


def http_request(url, method="GET", payload=None, timeout=30):
    data = None

    headers = {
        "Accept": "application/json",
    }

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers=headers,
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")

            if not body:
                return response.status, {}

            return response.status, json.loads(body)

    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"HTTP {error.code} from {url}\n{body}"
        ) from error

    except Exception as error:
        raise RuntimeError(
            f"Request failed for {url}\n{error}"
        ) from error


def wait_for_ghost():
    print(f"Waiting for Ghost at {GHOST_URL}...")

    deadline = time.time() + 300
    last_error = None

    while time.time() < deadline:
        try:
            status, data = http_request(
                READY_URL,
                method="GET",
                timeout=10,
            )

            if status == 200:
                print("Ghost is responding.")
                print(f"Site response: {data}")
                return

        except Exception as error:
            last_error = error
            print(f"Ghost not ready yet: {error}")

        time.sleep(5)

    raise RuntimeError(
        "Ghost did not become ready within 300 seconds.\n"
        f"Last error: {last_error}"
    )


def get_setup_status():
    status, data = http_request(
        SETUP_URL,
        method="GET",
        timeout=20,
    )

    print(f"Ghost setup response: {data}")

    setup = data.get("setup")

    if not isinstance(setup, list) or not setup:
        raise RuntimeError(
            f"Unexpected Ghost setup response format: {data}"
        )

    first_item = setup[0]

    if not isinstance(first_item, dict):
        raise RuntimeError(
            f"Unexpected Ghost setup item: {first_item}"
        )

    return first_item.get("status")


def create_owner():
    if not GHOST_EMAIL:
        raise RuntimeError("GHOST_EMAIL is missing.")

    if not GHOST_PASSWORD:
        raise RuntimeError("GHOST_PASSWORD is missing.")

    payload = {
        "setup": [
            {
                "name": "QA Automation Owner",
                "email": GHOST_EMAIL,
                "password": GHOST_PASSWORD,
                "blogTitle": "Ghost QA Automation",
            }
        ]
    }

    print("Creating fresh Ghost owner account...")
    print(f"Owner email: {GHOST_EMAIL}")

    status, data = http_request(
        SETUP_URL,
        method="POST",
        payload=payload,
        timeout=120,
    )

    print(f"Ghost setup POST returned HTTP {status}.")

    if data:
        print(f"Ghost setup POST response: {data}")

    if status not in (200, 201):
        raise RuntimeError(
            f"Ghost owner creation failed: HTTP {status}\n{data}"
        )

    print("Ghost owner account created successfully.")


def verify_owner_created():
    print("Verifying Ghost setup...")

    for _ in range(10):
        try:
            status = get_setup_status()

            if status is True:
                print("Ghost setup is complete.")
                return

        except Exception as error:
            print(f"Verification attempt failed: {error}")

        time.sleep(2)

    raise RuntimeError(
        "Ghost owner account was not confirmed after setup."
    )


def main():
    print("=== Ghost CI Bootstrap ===")
    print(f"Ghost URL: {GHOST_URL}")
    print(f"Test email: {GHOST_EMAIL}")

    if not GHOST_EMAIL:
        raise RuntimeError("GHOST_EMAIL is missing.")

    if not GHOST_PASSWORD:
        raise RuntimeError("GHOST_PASSWORD is missing.")

    wait_for_ghost()

    setup_status = get_setup_status()

    print(f"Ghost setup status: {setup_status}")

    if setup_status is True:
        print("Ghost is already initialized.")
        return

    if setup_status is False:
        create_owner()
        verify_owner_created()
        print("=== Ghost CI Bootstrap Complete ===")
        return

    raise RuntimeError(
        f"Unexpected Ghost setup status: {setup_status}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nBOOTSTRAP FAILED: {error}")
        sys.exit(1)