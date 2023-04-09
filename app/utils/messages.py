from dataclasses import dataclass


@dataclass
class Messages:
    USER_CREATED = "user created"
    USER_NOT_FOUND = "user not found"
    USER_ALREADY_EXISTS = "user already exists"
    USER_LOGOUT = "logout"
    ACCESS_DENIED = "access denied"

    INVALID_TOKEN = "invalid token"

    WRONG_PASSWORD = "wrong password"

    RECIPE_CREATED = "recipe created"
    RECIPE_UPDATED = "recipe updated"
    RECIPE_DELETED = "recipe deleted"
    RECIPE_NOT_FOUND = "recipe not found"
    RECIPE_PHOTO_UPLOADED = "recipe photo uploaded"

    STEP_NOT_FOUND = "step not found"

    REVIEW_SAVED = "review saved"
    REVIEW_ALREADY_LEFT = "review already left"
    REVIEW_NOT_FOUND = "review not found"

    NOT_FOUND = "not found"


messages = Messages()
