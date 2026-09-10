import json
import os
import sys
import time
import urllib.error
import urllib.request


GHOST_URL = os.getenv("GHOST_URL", "http://localhost:3001").rstrip("/")
GHOST_EMAIL = os.getenv("GHOST_EMAIL")
GHOST_PASSWORD = os.getenv("GHOST_PASSWORD")

SETUP_STATUS_URL = (
    f"{GHOST_URL}/ghost/api/admin/authentication/setup/"
)

SETUP_URL = (
    f"{GHOST_URL}/ghost/api/admin/authentication/setup/"
)


def get_setup_status():
    request = urllib.request.Request(
        SETUP_STATUS_URL,
        method="GET",
        headers={
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)

    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Ghost setup status failed: HTTP {error.code}\n{body}"
        )


def wait_for_ghost():
    print(f"Waiting for Ghost at {GHOST_URL}...")

    deadline = time.time() + 120

    while time.time() < deadline:
        try:
            status_code, data = get_setup_status()

            if status_code == 200:
                print(f"Ghost is ready: setup.status={data.get('setup', {}).get('status')}")
                return data

        except Exception:
            pass

        time.sleep(3)

    raise RuntimeError("Ghost did not become ready within 120 seconds.")


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

    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        SETUP_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_body = response.read().decode("utf-8")

            if response.status not in (200, 201):
                raise RuntimeError(
                    f"Ghost owner creation failed: HTTP {response.status}\n"
                    f"{response_body}"
                )

            print("Ghost owner account created successfully.")

    except urllib.error.HTTPError as error:
        response_body = error.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"Ghost owner creation failed: HTTP {error.code}\n"
            f"{response_body}"
        )


def main():
    print("=== Ghost CI Bootstrap ===")
    print(f"Ghost URL: {GHOST_URL}")
    print(f"Test email: {GHOST_EMAIL}")

    setup_data = wait_for_ghost()

    setup_status = (
        setup_data
        .get("setup", {})
        .get("status")
    )

    if setup_status is True:
        print("Ghost is already initialized.")
        return

    if setup_status is not False:
        print(f"Unexpected Ghost setup response: {setup_data}")
        sys.exit(1)

    create_owner()

    print("Ghost CI bootstrap completed.")


if __name__ == "__main__":
    main()