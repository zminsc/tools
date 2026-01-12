from http.client import HTTPConnection
import pathlib
import pytest
from subprocess import Popen, PIPE
import time
import socket

test_dir = pathlib.Path(__file__).parent.absolute()
root = test_dir.parent.absolute()


def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


@pytest.fixture(scope="module")
def static_server():
    """Start a local HTTP server for testing."""
    # Kill any existing process on port 8123
    if is_port_in_use(8123):
        import os
        os.system("fuser -k 8123/tcp 2>/dev/null")
        time.sleep(1)

    process = Popen(
        ["python3", "-m", "http.server", "8123", "--directory", str(root)],
        stdout=PIPE,
        stderr=PIPE,
    )

    # Wait for server to be ready
    retries = 10
    while retries > 0:
        try:
            conn = HTTPConnection("127.0.0.1", 8123, timeout=5)
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response is not None:
                break
        except (ConnectionRefusedError, OSError):
            time.sleep(0.5)
            retries -= 1
        finally:
            conn.close()

    if retries <= 0:
        process.terminate()
        process.wait()
        raise RuntimeError("Failed to start http server")

    yield process

    process.terminate()
    process.wait()
