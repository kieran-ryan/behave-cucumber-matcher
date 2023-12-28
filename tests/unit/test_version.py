"""Package version unit tests."""

import packaging.version
import pytest

from behave_cucumber_matcher.__version__ import __version__


@pytest.mark.parametrize(
    ("version_component", "version_type"),
    [
        (packaging.version.parse(__version__), packaging.version.Version),
        (packaging.version.parse(__version__).major, int),
        (packaging.version.parse(__version__).minor, int),
        (packaging.version.parse(__version__).micro, int),
    ],
)
def test_version_is_valid(version_component, version_type):
    """Package version is valid."""
    assert isinstance(version_component, version_type)
