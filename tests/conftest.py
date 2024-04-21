import pytest
import sys


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"console": "", "write_calls": 0}

    def fake_write(s):
        buffer["console"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, 'write', fake_write)
    return buffer
