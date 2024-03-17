"""Behave environment setup."""

from behave.matchers import use_step_matcher

from behave_cucumber_matcher import CUCUMBER_EXPRESSIONS_MATCHER

# Specify to use the Cucumber Expressions step matcher
use_step_matcher(CUCUMBER_EXPRESSIONS_MATCHER)
