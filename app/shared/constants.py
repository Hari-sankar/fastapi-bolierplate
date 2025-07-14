# Response Messages
RESPONSE_500 = "Internal Server Error"

# Descriptions
EMAIL_DESC = "Valid email address of the user."
PASSWORD_DESC = "Password of the user with a minimum length of 8 characters."
FIRST_NAME_DESC = "First name of the user."
LAST_NAME_DESC = "Last name of the user."
LIMIT_DESC = "Limit the number of returned users. Must be greater than 0."
OFFSET_DESC = "Number of users to skip. Must be 0 or more."
SEARCH_DESC = "Search term to filter users by."
SORT_DESC = "Sort users either in ascending (ASC) or descending (DESC) order."
TOKEN_DESC = "Verification Token"
PASSWORD_RESET_TOKEN_DESC = "Password Reset Token"
NEW_PASSWORD_DESC = "New Password"

# Examples
EMAIL_EXAMPLE = "user@domain.com"
PASSWORD_EXAMPLE = "yourpassword"
FIRST_NAME_EXAMPLE = "Don"
LAST_NAME_EXAMPLE = "John"
TOKEN_EXAMPLE = "sometoken"
NEW_PASSWORD_EXAMPLE = "newpassword"
LIMIT_EXAMPLE = 10
OFFSET_EXAMPLE = 0
SORT_EXAMPLE = "ASC"

# Error Messages
EMAIL_MISSING_ERROR = "Email field must not be empty"
INVALID_EMAIL_ERROR = "Invalid email format"
PASSWORD_MISSING_ERROR = "Password field must not be empty"
PASSWORD_LENGTH_ERROR = "Password must be at least 8 characters long"

