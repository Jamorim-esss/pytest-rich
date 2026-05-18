import pytest


@pytest.mark.skip("TODO")
def test_skip_decorator():
    pass


def test_skip_inline():
    pytest.skip("not now")


@pytest.mark.xfail(reason="known bug")
def test_xfail_expected():
    assert False


@pytest.mark.xfail(reason="unexpected")
def test_xpass_unexpected():
    assert True


@pytest.mark.xfail(reason="must fail", strict=True)
def test_xpass_strict():
    assert True
