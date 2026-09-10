Feature: Ghost post publishing

  Scenario: Owner publishes a new post
    Given I am logged into Ghost
    When I create and publish a new post
    Then the published post should appear in the Posts list