"""Fixtures etc."""
import pytest


@pytest.fixture()
def default_inbound():
    return {
        "msisdn": "12223334455",
        "text": "app: apps"
    }