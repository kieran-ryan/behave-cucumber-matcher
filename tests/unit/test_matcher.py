"""Matcher unit tests."""

import pytest
from behave.model_core import Argument
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry

from behave_cucumber_matcher.matcher import (
    CucumberExpressionMatcher,
    build_step_matcher,
)


class ArgumentEquivalence(Argument):
    """Class for equivalence testing Behave arguments."""

    def __eq__(self, other: Argument):
        """Check if two arguments are equivalent."""
        return (
            self.start == other.start
            and self.end == other.end
            and self.original == other.original
            and self.value == other.value
            and self.name == other.name
        )


@pytest.mark.parametrize(
    ("pattern", "step", "output"),
    [
        ("I have {int} cukes in my {word} now", "I have a non matching step", None),
        ("Step without arguments", "Step without arguments", []),
        (
            "I have {int} cukes in my {word} now",
            "I have 7 cukes in my belly now",
            [
                ArgumentEquivalence(
                    start=7,
                    end=8,
                    original="7",
                    value=7,
                ),
                ArgumentEquivalence(
                    start=21,
                    end=26,
                    original="belly",
                    value="belly",
                ),
            ],
        ),
    ],
)
def test_matches(pattern, step, output):
    """Test matches have appropriate outputs."""
    matcher = CucumberExpressionMatcher(
        func=lambda: None,
        pattern=pattern,
    )
    assert matcher.check_match(step) == output


def test_cucumber_expression_to_regex_pattern():
    """Test that no match is found."""
    matcher = CucumberExpressionMatcher(
        func=lambda: None,
        pattern="I have {int} cukes in my {word} now",
    )
    assert (
        matcher.regex_pattern
        == r"^I have ((?:-?\d+)|(?:\d+)) cukes in my ([^\s]+) now$"
    )


def test_build_matcher_without_parameter_type_registry():
    """Matcher built without parameter type registry does not throw exception."""
    matcher = build_step_matcher()
    assert matcher


def test_build_matcher_is_callable():
    """Matcher is callable."""
    registry = ParameterTypeRegistry()
    matcher = build_step_matcher(registry)
    assert callable(matcher)
    assert matcher(print, "I have {int} cukes in my {word} now")
