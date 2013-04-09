Feature: Testing Smartgrid
  Scenario: Homer wants to insert into the app his whole family
    Given Homer registers and reaches the smartgrid page
    When he clicks on the Add button
    Then the form for inserting a person is shown
    When he fills it with its "Homer" and submits
    Then he'll be back at the persons grid
    When he fills it with all the others
    | person_name |
    | Marge  |
    | Lisa   |
    | Bart   |
    | Maggie |
    Then the table will have "5" rows

  Scenario: Homer wants to assign Santa's Little Helper to Bart
    Given Homer reaching the smartgrid page
    When he chooses "Dogs" in the line corresponding to "Bart"
    Then no dogs are there for "Bart" yet
    When he clicks on the Add button
    Then he checks that "Bart" is in fact preselected as master
    When fills it with "Santa's Little Helper"
    And  submits it
    Then the table of dogs owned by "Bart" will have "1" row
