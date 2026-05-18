from __future__ import annotations

import pytest


def test_collect_error(rich_pytester):
    rich_pytester.makepyfile("""
    raise Exception("collect error")
    """)
    result = rich_pytester.runpytest()
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*ERROR collecting*"])


def test_collect_error_shown_with_no_summary(rich_pytester):
    """Collection errors must be visible even when --no-summary is used."""
    rich_pytester.makepyfile("""
    raise Exception("collect error")
    """)
    result = rich_pytester.runpytest("--no-summary")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*ERROR collecting*"])


class TestSetupTeardownErrors:
    # Setup errors fall into ``else: status = "running"`` at terminal.py:201
    # and never reach ``categorized_reports``. Teardown errors are ignored
    # entirely (no ``when == "teardown"`` branch in pytest_runtest_logreport).
    # The xfail strict markers flip to unexpected-pass when those branches land.

    @pytest.mark.xfail(
        strict=True, reason="Rich panel drops setup errors — terminal.py:201"
    )
    def test_setup_error_reported(self, rich_pytester, assert_rich_outcomes):
        rich_pytester.copy_example("test_basic.py")
        result = rich_pytester.runpytest("-k", "test_setup_error")
        assert result.ret != 0
        assert_rich_outcomes(result, errors=1)

    @pytest.mark.xfail(
        strict=True, reason="Rich panel drops teardown errors — terminal.py:190"
    )
    def test_teardown_error_reported(self, rich_pytester, assert_rich_outcomes):
        rich_pytester.copy_example("test_basic.py")
        result = rich_pytester.runpytest("-k", "test_teardown_error")
        assert result.ret != 0
        assert_rich_outcomes(result, errors=1)


class TestCollectionErrors:

    def test_partial_collection_error_shows_details(self, rich_pytester):
        rich_pytester.makepyfile(
            test_good="def test_pass(): pass",
            test_broken="raise ImportError('boom')",
        )
        result = rich_pytester.runpytest()
        assert result.ret != 0
        result.stdout.fnmatch_lines([
            "*ERROR collecting*test_broken*",
            "*ImportError: boom*",
        ])
