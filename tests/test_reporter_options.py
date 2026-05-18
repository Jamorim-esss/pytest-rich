from __future__ import annotations

import pytest


@pytest.fixture
def all_passing(rich_pytester):
    rich_pytester.copy_example("test_all_passing.py")
    return rich_pytester


class TestAllPassing:

    def test_no_failures_panel(self, all_passing, assert_rich_outcomes):
        result = all_passing.runpytest()
        assert result.ret == 0
        assert_rich_outcomes(result, passed=2)
        result.stdout.fnmatch_lines(["*SUCCEEDED*"])
        assert not any("FAILURES" in line for line in result.stdout.lines)

    def test_summary_panel_shown(self, all_passing):
        result = all_passing.runpytest()
        assert result.ret == 0
        result.stdout.fnmatch_lines(["*Summary*", "*Total Tests*"])


class TestVerboseMode:

    def test_verbose_shows_success_lines(self, all_passing):
        result = all_passing.runpytest("-v")
        assert result.ret == 0
        result.stdout.fnmatch_lines(["*SUCCESS*test_a*", "*SUCCESS*test_b*"])

    def test_non_verbose_hides_success_lines(self, all_passing):
        result = all_passing.runpytest()
        assert result.ret == 0
        assert not any("SUCCESS" in line for line in result.stdout.lines)


class TestNoHeaderNoSummary:

    def test_no_header_hides_platform_info(self, all_passing):
        result = all_passing.runpytest("--no-header")
        assert result.ret == 0
        assert not any("platform" in line for line in result.stdout.lines)

    def test_no_summary_hides_summary_panel(self, all_passing):
        result = all_passing.runpytest("--no-summary")
        assert result.ret == 0
        assert not any("Summary" in line for line in result.stdout.lines)

    def test_no_summary_still_shows_status_line(self, all_passing):
        result = all_passing.runpytest("--no-summary")
        assert result.ret == 0
        result.stdout.fnmatch_lines(["*SUCCEEDED*"])
