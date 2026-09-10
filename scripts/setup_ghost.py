import json
import os
import time
import urllib.error
import urllib.request


GHOST_URL = os.getenv("GHOST_URL", "http://localhost:3001").rstrip("/")
GHOST_EMAIL = os.getenv("GHOST_EMAIL")
GHOST_PASSWORD = os.getenv("GHOST_PASSWORD")

READY_URL = f"{GHOST_URL}/ghost/api/admin/site/"
SETUP_URL = f"{GHOST_URL}/ghost/api/admin/authentication/setup/"


def request_json(url, method="GET", payload=None, timeout=30):
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
            return response.status, json.loads(body)

    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {error.code} from {url}\n{body}"
        ) from error

    except Exception as error:
        raise RuntimeError(
            f"Request failed: {url}\n{error}"
        ) from error


def wait_for_ghost():
    print(f"Waiting for Ghost at {GHOST_URL}...")

    deadline = time.time() + 300

    last_error = None

    while time.time() < deadline:
        try:
            status, data = request_json(
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


def check_setup_status():
    status, data = request_json(
        SETUP_URL,
        method="GET",
        timeout=20,
    )

    print(f"Ghost setup response: {data}")

    setup = data.get("setup", {})

    return setup.get("status")


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

    try:
        status, data = request_json(
            SETUP_URL,
            method="POST",
            payload=payload,
            timeout=120,
        )

        print(f"Ghost setup POST returned HTTP {status}.")
        print(f"Ghost setup response: {data}")

    except Exception as error:
        print(f"Ghost setup request reported an error: {error}")
        print("Checking whether the account was created anyway...")

        time.sleep(5)

        setup_status = check_setup_status()

        if setup_status is True:
            print("Ghost setup completed successfully.")
            return

        raise


def main():
    print("=== Ghost CI Bootstrap ===")
    print(f"Ghost URL: {GHOST_URL}")
    print(f"Test email: {GHOST_EMAIL}")

    wait_for_ghost()

    setup_status = check_setup_status()

    if setup_status is True:
        print("Ghost is already initialized.")
        return

    if setup_status is False:
        create_owner()
        print("Ghost owner account created successfully.")
        return

    raise RuntimeError(
        f"Unexpected Ghost setup status: {setup_status}"
    )


if __name__ == "__main__":
    main()