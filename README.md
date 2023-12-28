# Behave Cucumber Matcher

[![Release version](https://img.shields.io/badge/dynamic/json?color=green&label=version&query=%24.info.version&url=https%3A%2F%2Ftest.pypi.org%2Fpypi%2Fbehave-cucumber-matcher%2Fjson)](https://test.pypi.org/pypi/behave-cucumber-matcher)
![License](https://img.shields.io/badge/license-MIT-blue)
[![Python versions](https://img.shields.io/pypi/pyversions/behave-cucumber-matcher.svg)](https://pypi.org/pypi/behave-cucumber-matcher)
![Supported platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Windows%20%7C%20Linux-green)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Pipeline status](https://github.com/kieran-ryan/behave-cucumber-matcher/actions/workflows/main.yml/badge.svg)

Behave step matcher for [Cucumber Expressions](https://github.com/cucumber/cucumber-expressions).

## Installation

`behave-cucumber-matcher` is available via [PyPI](https://pypi.org/project/behave_cucumber_matcher/):

```console
pip install behave-cucumber-matcher
```

## Usage

Import and patch the matcher into Behave inside `environment.py` in your `features` directory.

```python
from behave.matchers import use_step_matcher, matcher_mapping
from behave_cucumber_matcher import build_step_matcher
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry

# Initialise a Cucumber Expressions parameter registry
parameter_registry = ParameterTypeRegistry()

# Create the step matcher to pass to behave
step_matcher = build_step_matcher(parameter_registry)

# Patch the step matcher into behave
matcher_mapping["cucumber_expressions"] = step_matcher

# Specify to use the Cucumber Expressions step matcher
use_step_matcher("cucumber_expressions")
```

Create a scenario inside `color.feature` in your `features` directory:

```gherkin
Feature: Color selection

  Rule: User can select a profile color

    Scenario: User selects a valid color
      Given I am on the profile settings page
      When I select the theme colour "red"
      Then the profile colour should be "red"
```

Create step definitions inside `color.py` in your `features/steps` directory:

```python
from behave import given, then, when
from cucumber_expressions.parameter_type import ParameterType

from environment import parameter_registry

# Define the parameter type
color = ParameterType(
    name="color",
    regexp="red|blue|yellow",
    type=str,
    transformer=lambda s: s,
    use_for_snippets=True,
    prefer_for_regexp_match=False,
)

# Pass the parameter type to the registry instance
parameter_registry.define_parameter_type(color)

@given("I am on the profile customisation/settings page")
def step_given(context):
    assert True

# Reference the parameter type in the step definition pattern
@when('I select the theme colo(u)r "{color}"')
def step_when(context, selected_color):
    assert selected_color
    context.selected_color = selected_color

@then('the profile colo(u)r should be "{color}"')
def step_then(context, displayed_color):
    assert displayed_color
    assert context.selected_color == displayed_color
```

The necessary files are now in place to execute your gherkin scenario.

```console
repository/
  └── features/
      ├── steps/
      │   └── color.py
      ├── environment.py
      └── color.feature
```

Finally, execute Behave. The scenario will run with the step definitions using the Cucumber Expressions parameter type.

```console
$ behave features
Feature: Color selection # features/Gherkin.feature:1
  Rule: User can select a profile color
  Scenario: User selects a valid color      # features/Gherkin.feature:5
    Given I am on the profile settings page # features/steps/color.py:20 0.000s
    When I select the theme colour "red"    # features/steps/color.py:26 0.000s
    Then the profile colour should be "red" # features/steps/color.py:32 0.000s

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
3 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.001s
```

For detailed usage of _behave_, see the [official documentation](https://behave.readthedocs.io).

## Acknowledgements

Based on the Behave step matcher base class and built on the architecture of [cuke4behave](https://gitlab.com/cuke4behave/cuke4behave) by [Dev Kumar Gupta](https://github.com/mrkaiser), with extended type hints, a fix for detecting patterns without arguments, a default parameter type registry, additional documentation for arguments and return types and direct import of the matcher at package level rather than via its module.

## License

`behave-cucumber-matcher` is licensed under the [MIT License](https://opensource.org/licenses/MIT)
