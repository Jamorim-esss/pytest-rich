from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    "k_expr",
    [
        pytest.param("test_nested_failure", id="one-level"),
        pytest.param("test_doubly_nested_failures", id="two-levels"),
        pytest.param("test_triply_nested_failures", id="three-levels"),
    ],
)
def test_nested_function_failures(rich_pytester, assert_rich_outcomes, k_expr):
    rich_pytester.copy_example("test_basic.py")
    result = rich_pytester.runpytest("-k", k_expr)
    assert result.ret == 1
    assert_rich_outcomes(result, failed=1)
    result.stdout.fnmatch_lines([
        "*assert False*",
        "*Summary*",
    ])


class TestMultipleFiles:

    def test_two_files_both_reported(self, rich_pytester, assert_rich_outcomes):
        rich_pytester.makepyfile(
            test_alpha="def test_a(): pass",
            test_beta="def test_b(): pass",
        )
        result = rich_pytester.runpytest()
        assert result.ret == 0
        assert_rich_outcomes(result, passed=2)
        result.stdout.fnmatch_lines(["*%*test_alpha*", "*%*test_beta*"])

    def test_mixed_outcomes_across_files(self, rich_pytester, assert_rich_outcomes):
        rich_pytester.makepyfile(
            test_ok="def test_pass(): pass",
            test_bad="def test_fail(): assert False",
        )
        result = rich_pytester.runpytest()
        assert result.ret == 1
        assert_rich_outcomes(result, passed=1, failed=1)
