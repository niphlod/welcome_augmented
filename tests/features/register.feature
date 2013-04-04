Feature: Registering and login to welcome_augmented

  Scenario: login and register
    Given Homer accesses the app
      When Homer reaches the registration page
      Then he fills the form with an incorrect email
        | first_name | last_name | email | password | password_two |
        | Homer      | Simpson   | homer | mostdifficultpassword | mostdifficultpassword |
      And  an error will be returned
      When he re-fills the form with the correct email
        | first_name | last_name | email | password | password_two |
        | Homer      | Simpson   | homer@localhost | mostdifficultpassword | mostdifficultpassword |
      Then he will check that the password is reported as strong enough
      And  he will submit it
      And  he will be registered and taken to the index page
