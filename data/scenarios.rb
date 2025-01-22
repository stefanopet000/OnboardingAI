Scenario: [Authentication] The user logs in using an email address
Given I am a registered user
When I enter my email address and press enter
Then I should be able to log in to the application

Scenario: Password reset for a user
Given I forgot my password
When I click on the "Forgot Password" link
Then I should receive an email with a reset link

Scenario: Viewing the user profile
Given I am logged in
When I navigate to the profile page
Then I should see my profile details

Scenario: Adding an item to the shopping cart
Given I am browsing items
When I click "Add to Cart" on an item
Then the item should appear in my shopping cart

Scenario: Checking out items in the cart
Given I have items in my shopping cart
When I click "Checkout" and provide payment details
Then my order should be placed successfully

Scenario: Searching for products
Given I am on the homepage
When I type a product name into the search bar and press enter
Then I should see relevant search results

Scenario: Updating account details
Given I am logged in
When I go to the account settings page and edit my details
Then my changes should be saved

Scenario: Logging out of the application
Given I am logged in
When I click the "Logout" button
Then I should be logged out and redirected to the login page

Scenario: Submitting feedback
Given I am on the feedback page
When I fill out the feedback form and click "Submit"
Then my feedback should be recorded

Scenario: Viewing order history
Given I have placed orders in the past
When I go to the order history page
Then I should see a list of my past orders