import logging
import os
import pytest
import sys
from subprocess import CalledProcessError

import flit6


def test_main_shortcircuits_on_py3(mocker):
    mocker.patch("flit6.sys.version_info", (3,))
    sys.modules["flit"] = mock_flit = mocker.MagicMock()
    flit6.main()
    mock_flit.main.assert_called_once_with()


def test_main(mocker):
    mocker.patch("flit6.sys.version_info", (2, 7))
    mocker.patch("sys.argv", ["flit6", "install"])
    mock = mocker.MagicMock()
    mock.attach_mock(mocker.patch("flit6.validate_env"), "validate")
    mock.attach_mock(mocker.patch("flit6.clean"), "clean")
    mock.attach_mock(mocker.patch("flit6.build", return_value="./somefile"), "build")
    mock.attach_mock(mocker.patch("flit6.install"), "install")
    flit6.main()
    mock.assert_has_calls([
        mocker.call.validate(),
        mocker.call.clean(),
        mocker.call.build(),
        mocker.call.install("./somefile"),
    ])


def test_clean(tmpdir):
    fname = "myapp-0.1-py2.py3-none-any.whl"
    subdir = tmpdir.ensure("dist", dir=True)
    dist_file = subdir.join(fname)
    dist_file.ensure(file=True)
    file = str(tmpdir / "dist" / fname)
    assert os.path.isdir("./dist")
    assert os.path.isfile(file)
    flit6.clean()
    assert not os.path.isdir("./dist")
    assert not os.path.isfile(file)


def test_install(mocker):
    check_call = mocker.patch("flit6.subprocess.check_call")
    flit6.install("myapp.tar.gz")
    check_call.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", "myapp.tar.gz"]
    )


def test_build_ok(mocker, tmpdir):
    tmpdir.ensure("dist/myapp-0.1-py2.py3-none-any.whl", file=True)
    check_output = mocker.patch("flit6.subprocess.check_output")
    fname = flit6.build()
    check_output.assert_called_once_with("python3 -m flit build".split())
    assert fname == "./dist/myapp-0.1-py2.py3-none-any.whl"


def test_build_sdist(mocker, tmpdir):
    tmpdir.ensure("dist/myapp-0.1.tar.gz", file=True)
    check_output = mocker.patch("flit6.subprocess.check_output")
    fname = flit6.build()
    check_output.assert_called_once_with("python3 -m flit build".split())
    assert fname == "./dist/myapp-0.1.tar.gz"


def test_build_multiple(mocker, tmpdir, caplog):
    tmpdir.ensure("dist/myapp-0.1a-py2.py3-none-any.whl", file=True)
    tmpdir.ensure("dist/myapp-0.1b-py2.py3-none-any.whl", file=True)
    mocker.patch("flit6.subprocess.check_output")
    fname = flit6.build()
    assert fname == "./dist/myapp-0.1b-py2.py3-none-any.whl"
    logged = caplog.record_tuples[-1]
    assert logged[0:2] == ("flit6", logging.WARNING)
    assert logged[2].startswith("found many wheels, returning newest one")


def test_build_multiple_sdist(mocker, tmpdir, caplog):
    tmpdir.ensure("dist/myapp-0.1a.tar.gz", file=True)
    tmpdir.ensure("dist/myapp-0.1b.tar.gz", file=True)
    mocker.patch("flit6.subprocess.check_output")
    fname = flit6.build()
    assert fname == "./dist/myapp-0.1b.tar.gz"
    logged = caplog.record_tuples[-1]
    assert logged[0:2] == ("flit6", logging.WARNING)
    assert logged[2].startswith("found many sdists, returning newest one")


def test_build_no_dist(mocker, caplog):
    mocker.patch("flit6.subprocess.check_output")
    with pytest.raises(SystemExit, match="^1$"):
        flit6.build()
    assert caplog.record_tuples[-1] == ("flit6", logging.ERROR, "no dist generated")


def test_validate_env_ensures_running_on_py2(mocker):
    mocker.patch("flit6.sys.version_info").major = 3
    with pytest.raises(SystemExit, match="^flit6 itself should only be run in python2$"):
        flit6.validate_env()


def test_validate_env_ensures_pip_is_installed(tmpdir, monkeypatch, fake_py2):
    sys.modules.pop("pip", None)
    tmpdir.join("pip.py").write("raise ImportError")
    monkeypatch.syspath_prepend(tmpdir)
    with pytest.raises(SystemExit, match="^flit6 requires a python2 installation with pip$"):
        flit6.validate_env()


def test_validate_env_ensures_python3_avail(mocker, fake_py2):
    check_output = mocker.patch("flit6.subprocess.check_output", side_effect=CalledProcessError(1, 'wtf'))
    with pytest.raises(SystemExit, match="^flit6 requires python3 available to subprocess$"):
        flit6.validate_env()
    check_output.assert_called_once_with("python3 -V".split())


def test_validate_env_ensures_python3_has_flit(mocker, fake_py2):
    effect = ["Python 3.7.1\n", CalledProcessError(1, 'wtf')]
    check_output = mocker.patch("flit6.subprocess.check_output", side_effect=effect)
    with pytest.raises(SystemExit, match="^flit6 requires a python3 flit installation$"):
        flit6.validate_env()
    check_output.assert_has_calls([
        mocker.call("python3 -V".split()),
        mocker.call("python3 -m flit -V".split()),
    ])


def test_validate_env_all_ok(mocker, fake_py2):
    effect = ["Python 3.7.1\n", "Flit 1.2.1\n"]
    mocker.patch("flit6.subprocess.check_output", side_effect=effect)
    flit6.validate_env()
