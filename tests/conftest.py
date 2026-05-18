from __future__ import annotations

import pytest

pytest_plugins = "pytester"


@pytest.fixture
def assert_rich_outcomes() -> Callable[..., None]:
    """Verify test outcomes by inspecting the Rich summary panel."""
    def _check(result: pytest.RunResult, **expected: int) -> None:
        for category, count in expected.items():
            label = category.title()
            matched = any(
                f"  {count}  {label}" in line
                for line in result.stdout.lines
            )
            assert matched, (
                f"Expected '  {count}  {label}' in Rich summary, "
                f"but not found in output"
            )
    return _check


@pytest.fixture
def rich_pytester(pytester):
    """Replace the standard reporter with the Rich one.

    Using ``--rich`` is not enough because pytester captures stdout,
    so ``sys.stdout.isatty()`` returns False and the plugin never activates.
    """
    pytester.makeconftest("""
        import pytest
        from pytest_rich.terminal import RichTerminalReporter

        @pytest.hookimpl(trylast=True)
        def pytest_configure(config):
            standard_reporter = config.pluginmanager.getplugin("terminalreporter")
            config.pluginmanager.unregister(standard_reporter)
            config.pluginmanager.register(
                RichTerminalReporter(config), "rich-terminal-reporter"
            )
    """)
    return pytester
