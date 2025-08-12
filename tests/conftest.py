import pytest


@pytest.fixture
def sample_records():
    return [
        {"url": "/test", "response_time": 0.1, "@timestamp": "2023-01-01T00:00:00"},
        {"url": "/test", "response_time": 0.2, "@timestamp": "2023-01-01T00:01:00"},
        {"url": "/other", "response_time": 0.3, "@timestamp": "2023-01-02T00:00:00"},
    ]
