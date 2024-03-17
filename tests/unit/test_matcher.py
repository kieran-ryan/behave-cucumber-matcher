"""Matcher unit tests."""

import behave.matchers
import pytest
from behave.model_core import Argument
from cucumber_expressions.parameter_type import ParameterType
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry

from behave_cucumber_matcher.matcher import (
    CUCUMBER_EXPRESSIONS_MATCHER,
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
    assert callable(matcher)
    assert matcher(print, "I have {int} cukes in my {word} now")


def test_build_matcher_is_callable():
    """Matcher is callable."""
    registry = ParameterTypeRegistry()
    matcher = build_step_matcher(registry)
    assert callable(matcher)
    assert matcher(print, "I have {int} cukes in my {word} now")


def test_matcher_patched_into_behave():
    """Matcher is patched into Behave step matchers."""
    assert CUCUMBER_EXPRESSIONS_MATCHER in behave.matchers.matcher_mapping


def test_no_exception_without_parameter_type_defaults():
    """Compatible with earlier Cucumber Expressions versions.

    Cucumber Expressions below 17.0.2 do not set expected defaults
    for `use_for_snippets` and `prefer_for_regexp_match` in the
    parameter type.
    """
    ParameterType(
        name="color",
        regexp="red|blue|yellow",
        type=str,
        transformer=lambda s: s,
    )
