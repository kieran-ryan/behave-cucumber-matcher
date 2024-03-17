"""Step definitions for profile colour configuration."""

from behave import given, then, when
from cucumber_expressions.parameter_type import ParameterType

# Define the parameter type
ParameterType(
    name="color",
    regexp="red|blue|yellow",
    type=str,
    transformer=lambda s: s,
)


@given("I am on the profile customisation/settings page")
def step_given(_):
    """Navigate to the profile configuration page."""
    assert True


# Reference the parameter type in the step definition pattern
@when('I select the theme colo(u)r "{color}"')
def step_when(context, selected_color: str):
    """Select a colour on the profile configuration page."""
    assert selected_color
    context.selected_color = selected_color


@then('the profile colo(u)r should be "{color}"')
def step_then(context, displayed_color: str):
    """Check the displayed colour on the profile configuration page."""
    assert displayed_color
    assert context.selected_color == displayed_color
