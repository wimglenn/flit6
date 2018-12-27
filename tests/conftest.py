import os

import pytest


@pytest.fixture(autouse=True)
def chtmpdir(tmpdir):
    old = os.getcwd()
    try:
        tmpdir.chdir()
        yield
    finally:
        os.chdir(old)


@pytest.fixture
def fake_py2(mocker):
    mocker.patch("flit6.sys.version_info").major = 2
