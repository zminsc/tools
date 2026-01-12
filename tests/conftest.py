from http.client import HTTPConnection
import pathlib
import pytest
from subprocess import Popen, PIPE
import time

test_dir = pathlib.Path(__file__).parent.absolute()
root = test_dir.parent.absolute()


@pytest.fixture(scope="module")
def static_server():
    """Start a local HTTP server for testing."""
    process = Popen(
        ["python", "-m", "http.server", "8123", "--directory", str(root)],
        stdout=PIPE,
        stderr=PIPE,
    )
    retries = 5
    while retries > 0:
        conn = HTTPConnection("127.0.0.1:8123")
        try:
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response is not None:
                yield process
                break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1

    if not retries:
        raise RuntimeError("Failed to start http server")
    else:
        process.terminate()
        process.wait()
