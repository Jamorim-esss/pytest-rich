import pytest


def test_outcomes(pytester):
    pytester.copy_example("test_basic.py")

    outcomes = {
        "passed": 3,
        "skipped": 4,
        "failed": 2,
        "errors": 2,
        "xpassed": 1,
        "xfailed": 3,
    }

    without_rich = pytester.runpytest()
    with_rich = pytester.runpytest("--rich")

    without_rich.assert_outcomes(**outcomes) == with_rich.assert_outcomes(**outcomes)


def test_collect_error(pytester):
    pytester.makepyfile("""
    raise Exception("collect error")
    """)

    without_rich = pytester.runpytest()
    with_rich = pytester.runpytest("--rich")

    without_rich.assert_outcomes(errors=1) == with_rich.assert_outcomes(errors=1)


@pytest.fixture
def rich_pytester(pytester):
    """Register the Rich reporter alongside the standard one.

    Using ``--rich`` is not enough because pytester captures stdout,
    so ``sys.stdout.isatty()`` returns False and the plugin never activates.
    """
    pytester.makeconftest("""
        import pytest
        from pytest_rich.terminal import RichTerminalReporter

        @pytest.hookimpl(trylast=True)
        def pytest_configure(config):
            config.pluginmanager.register(
                RichTerminalReporter(config), "rich-terminal-reporter"
            )
    """)
    return pytester


@pytest.mark.parametrize(
    "test_code, expected_outcomes, expected_ret",
    [
        pytest.param(
            '@pytest.mark.skip("TODO")\ndef test_it(): pass',
            {"skipped": 1},
            0,
            id="skip-decorator",
        ),
        pytest.param(
            'def test_it(): pytest.skip("not now")',
            {"skipped": 1},
            0,
            id="skip-inline",
        ),
        pytest.param(
            '@pytest.mark.xfail(reason="known bug")\ndef test_it(): assert False',
            {"xfailed": 1},
            0,
            id="xfail",
        ),
        pytest.param(
            '@pytest.mark.xfail(reason="unexpected")\ndef test_it(): assert True',
            {"xpassed": 1},
            0,
            id="xpass",
        ),
        pytest.param(
            '@pytest.mark.xfail(reason="must fail", strict=True)\ndef test_it(): assert True',
            {"failed": 1},
            1,
            id="xpass-strict",
        ),
    ],
)
def test_skip_xfail_do_not_crash(
    rich_pytester, test_code, expected_outcomes, expected_ret
):
    rich_pytester.makepyfile(f"import pytest\n{test_code}")
    result = rich_pytester.runpytest()
    assert result.ret == expected_ret
    result.assert_outcomes(**expected_outcomes)
    result.stdout.fnmatch_lines(["*Summary*"])
