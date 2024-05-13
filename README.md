# LanguageLearningApp
This repo contains Backend API code for the Application.

# User Authentication and Learning Progress API

This repository contains a simple Flask-based API for user authentication and tracking learning progress. It includes endpoints for user registration, login, user profiles, language selection, and learning material management.

## Endpoints

1. Register User
    - Endpoint: `/api/auth/register`
    - Method: POST
    - Purpose: Registers a new user.
    - Request Data: Expects a JSON payload containing a username and password.
    - Response:
        - If successful, returns a message indicating successful registration (status code 201).
        - If missing username or password, returns an error message (status code 400).
        - If the username already exists, returns an error message (status code 400).

2. Login User
    - Endpoint: `/api/auth/login`
    - Method: POST
    - Purpose: Logs in a user.
    - Request Data: Expects a JSON payload containing a username and password.
    - Response:
        - If successful, generates a unique session ID for the user and redirects to the language selection endpoint (status code 200).
        - If invalid username or password, returns an error message (status code 401).
        - If missing username or password, returns an error message (status code 400).

3. User Profile
    - Endpoint: `/api/auth/users`
    - Method: GET
    - Purpose: Retrieves user profiles.
    - Response:
        - Returns a list of user profiles (status code 200).
        - If an error occurs, returns an error message (status code 500).

4. Supported Languages
    - Endpoint: `/api/languages`
    - Method: GET
    - Purpose: Retrieves supported languages.
    - Response:
        - Returns a list of supported languages (status code 200).
        - If an error occurs, returns an error message (status code 500).

5. Manage Learning Material
    - Endpoint: `/api/learning/materials/<string:language_code>`
    - Method: GET
    - Purpose: Retrieves, updates, or deletes learning material for a specific language.
    - Request Parameter: `language_code` (e.g., "en" for English)
    - Response:
        - Returns learning material for the specified language (status code 200).
        - If an error occurs, returns an error message (status code 500).

6. Update Learning Progress
    - Endpoint: `/api/learning/materials/user_progress_update/`
    - Method: POST
    - Purpose: Updates a specific user's learning progress.
    - Request Data:
        - Expects a JSON payload with the following fields (all are required):
            - `username`: The username of the user.
            - `languages`: A list of languages the user is learning.
            - `lessons`: A list of lessons the user has completed.
            - `score`: An optional score (default is 0).
            - `completed`: An optional flag indicating whether the user has completed the learning (default is `False`).
    - Response:
        - If successful, returns a message indicating the number of modifications made (status code 200).
        - If incomplete data is provided, returns an error message (status code 400).
        - If the user does not exist, returns an error message (status code 400).

7. Logout User
    - Endpoint: `/api/auth/logout`
    - Method: POST
    - Purpose: Logs out a user (assuming you are using Flask session for user authentication).
    - Request Data:
        - Expects a JSON payload containing the `username`.
    - Response:
        - If the user is logged in, removes the user from the session and returns a success message (status code 200).
        - If the user is not logged in, returns an error message (status code 401).

## Usage

1. Clone this repository.
2. Install the required dependencies (`Flask`, `pymongo`, etc.).
3. Set up your MongoDB connection.
4. Run the Flask app (`python app.py`).

Feel free to enhance and adapt this codebase to fit your project's needs! 😊
