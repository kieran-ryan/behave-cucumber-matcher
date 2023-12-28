"""Behave environment setup."""

from behave.matchers import matcher_mapping, use_step_matcher
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry

from behave_cucumber_matcher import build_step_matcher

# Initialise a Cucumber Expressions parameter registry
parameter_registry = ParameterTypeRegistry()

# Create the step matcher to pass to behave
step_matcher = build_step_matcher(parameter_registry)

# Patch the step matcher into behave
matcher_mapping["cucumber_expressions"] = step_matcher

# Specify to use the Cucumber Expressions step matcher
use_step_matcher("cucumber_expressions")
