from __future__ import annotations


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

    def test_setup_error_does_not_crash(self, rich_pytester):
        """The reporter must not crash on fixture lookup errors.

        Note: the Rich reporter currently does NOT display setup errors
        in the output (bug — setup failures are silently swallowed).
        This will be addressed in Phase 2 (#74).
        """
        rich_pytester.copy_example("test_basic.py")
        result = rich_pytester.runpytest("-k", "test_setup_error")
        assert result.ret != 0
        result.stdout.fnmatch_lines(["*FAILED*"])

    def test_teardown_error_does_not_crash(self, rich_pytester):
        """The reporter must not crash when a fixture teardown raises.

        Note: the Rich reporter currently does NOT display teardown
        errors — the test shows as passed despite the teardown failure.
        This will be addressed in Phase 2 (#74).
        """
        rich_pytester.copy_example("test_basic.py")
        result = rich_pytester.runpytest("-k", "test_teardown_error")
        assert result.ret != 0
        result.stdout.fnmatch_lines(["*Summary*"])


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
