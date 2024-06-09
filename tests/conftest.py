from typing import Protocol

import pytest
import sys


class LoggerProtocol(Protocol):

    def debug(self, msg, *args, **kwargs) -> None:
        ...

    def info(self, msg, *args, **kwargs) -> None:
        ...

    def warning(self, msg, *args, **kwargs) -> None:
        ...

    def error(self, msg, *args, **kwargs) -> None:
        ...

    def critical(self, msg, *args, **kwargs) -> None:
        ...


class TestLogger(LoggerProtocol):

    def debug(self, msg, *args, **kwargs) -> None:
        pass

    def info(self, msg, *args, **kwargs) -> None:
        pass

    def warning(self, msg, *args, **kwargs) -> None:
        pass

    def error(self, msg, *args, **kwargs) -> None:
        pass

    def critical(self, msg, *args, **kwargs) -> None:
        pass


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"console": "", "write_calls": 0}

    def fake_write(s):
        buffer["console"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, 'write', fake_write)
    return buffer


@pytest.fixture
def fake_logger():
    return TestLogger()
