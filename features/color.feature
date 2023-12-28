Feature: Color selection

  Rule: User can select a profile color

    Scenario: User selects a valid color
      Given I am on the profile settings page
      When I select the theme colour "red"
      Then the profile colour should be "red"
