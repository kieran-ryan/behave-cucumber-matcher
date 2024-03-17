# -*- coding: utf-8 -*-
"""Behave step definition matcher for Cucumber Expressions."""

from typing import Any, Callable, List, Optional

import cucumber_expressions.parameter_type
from behave.matchers import Matcher, matcher_mapping
from behave.model_core import Argument
from cucumber_expressions.expression import CucumberExpression
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry

CUCUMBER_EXPRESSIONS_MATCHER = "cucumber_expressions"

parameter_registry = ParameterTypeRegistry()


class ParameterTypeOverrides(cucumber_expressions.parameter_type.ParameterType):
    """Matcher compatibility for Cucumber Expressions parameter types."""

    def __init__(  # noqa: D107
        self,
        *args,
        # Fixes missing defaults in Cucumber Expressions below 17.0.2
        # See https://github.com/cucumber/cucumber-expressions/pull/259
        use_for_snippets: bool = True,
        prefer_for_regexp_match: bool = False,
        **kwargs,
    ):
        super().__init__(
            *args,
            use_for_snippets=use_for_snippets,
            prefer_for_regexp_match=prefer_for_regexp_match,
            **kwargs,
        )


cucumber_expressions.parameter_type.ParameterType = ParameterTypeOverrides


class CucumberExpressionMatcher(Matcher):
    """Matcher class that uses Cucumber Expressions."""

    def __init__(
        self,
        func: Callable,
        pattern: str,
        parameter_type_registry: Optional[ParameterTypeRegistry] = None,
    ):
        """Initialise CucumberExpressionMatcher.

        Args:
            func: The step function the pattern is being attached to.
            pattern: The match pattern attached to the step function.
            parameter_type_registry: The Cucumber parameter type registry to use.
        """
        super(CucumberExpressionMatcher, self).__init__(func, pattern)
        self.parameter_type_registry = (
            parameter_type_registry or ParameterTypeRegistry()
        )
        self.__cucumber_expression = CucumberExpression(
            pattern,
            self.parameter_type_registry,
        )

    def check_match(self, step: str) -> Optional[List[Argument]]:
        """Check step matches this step pattern.

        Args:
            step: The step to check.

        Returns:
            A list containing any arguments if the step matches the pattern, else None.
        """
        result = self.__cucumber_expression.match(step)
        if result is None:
            # No match
            return None
        return [
            Argument(
                start=argument.group.start,
                end=argument.group.end,
                original=str(argument.value),
                value=argument.value,
                # All Cucumber arguments are treated as anonymous.
                # No named keyword arguments. Thus `name=None`.
                name=None,
            )
            for argument in result
        ]

    @property
    def regex_pattern(self) -> str:
        """Return the used textual regex pattern of the Cucumber Expression."""
        return self.__cucumber_expression.regexp


def build_step_matcher(
    parameter_type_registry: Optional[ParameterTypeRegistry] = None,
) -> Callable[[Callable[..., Any], str], CucumberExpressionMatcher]:
    """Build a Behave step matcher for Cucumber Expressions.

    Args:
        parameter_type_registry: The Cucumber parameter type registry to use.

    Returns:
        A function that can be used as a step matcher.
    """

    def step_matcher(
        func: Callable[..., Any],
        pattern: str,
    ) -> CucumberExpressionMatcher:
        return CucumberExpressionMatcher(
            func,
            pattern,
            parameter_type_registry=parameter_type_registry,
        )

    return step_matcher


# Register the Cucumber Expressions step matcher with Behave
step_matcher = build_step_matcher(parameter_registry)
matcher_mapping[CUCUMBER_EXPRESSIONS_MATCHER] = step_matcher
