# Workout Tracker Backend

## Description

A Flask REST API for a workout tracking application. The API provides user registration and login using JSON Web Tokens (JWT), secure password hashing, and workout management.

Authenticated users can create, view, update, and delete their workouts. Each workout belongs to its owner, and pagination is supported when listing workouts.

## Features

- User registration and login.
- Password hashing with Flask-Bcrypt.
- JWT-based authentication for protected routes.
- Create, retrieve, update, and delete workouts.
- User-specific workout access and ownership enforcement.
- Paginated workout listings.
- Database migrations with Flask-Migrate.
- Database seeding with sample users and workouts.
- Automated tests using pytest.

## Technologies

- Python 3.8
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- SQLite
- pytest

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/kgee254/workout-tracker-backend.git
cd workout-tracker-backend
```

### 2. Install dependencies

Install Pipenv if it is not already installed:

```bash
pip install pipenv
```

Install the project's dependencies:

```bash
pipenv install
pipenv shell
```

If you are already using the project's virtual environment, you can skip activating another environment.

### 3. Configure the JWT secret

The application uses the `JWT_SECRET_KEY` environment variable to sign access tokens.

For local development, set a secret in your terminal:

```bash
export JWT_SECRET_KEY="replace-with-a-long-random-secret"
```

Use a securely generated secret in real deployments. Never commit production secrets to GitHub.

### 4. Set up the database

Initialize the database tables by applying the existing migrations:

```bash
flask --app app db upgrade
```

If you need to create a new migration after changing the models, run:

```bash
flask --app app db migrate -m "Describe your model changes"
flask --app app db upgrade
```

The project uses SQLite for database storage.

### 5. Seed the database

To populate the database with sample users and workouts, run:

```bash
python seed.py
```

The seed script creates sample accounts and workouts. Use the credentials specified in `seed.py` when testing the seeded accounts.

### 6. Start the API

Run:

```bash
python app.py
```

The development server runs at:

`http://127.0.0.1:5000`

## API Endpoints

All request and response bodies use JSON unless otherwise specified.

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/signup` | Register a new user | Not required |
| POST | `/login` | Log in and receive a JWT access token | Not required |
| GET | `/me` | Retrieve the authenticated user's details | Required |

#### Register a user

`POST /signup`

Example request:

```json
{
  "username": "newuser",
  "password": "password123"
}
```

Successful registration returns HTTP `201 Created`.

#### Log in

`POST /login`

Example request:

```json
{
  "username": "newuser",
  "password": "password123"
}
```

The response includes an `access_token`. Include this token in the Authorization header when accessing protected endpoints.

#### Retrieve the current user

`GET /me`

Requires a valid JWT access token.

### Workouts

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/workouts` | List the authenticated user's workouts | Required |
| GET | `/workouts/<workout_id>` | Retrieve a specific workout | Required |
| POST | `/workouts` | Create a workout | Required |
| PATCH | `/workouts/<workout_id>` | Update a workout | Required |
| DELETE | `/workouts/<workout_id>` | Delete a workout | Required |

#### Create a workout

`POST /workouts`

Example request:

```json
{
  "exercise": "Push-ups",
  "duration": 15,
  "notes": "Three sets"
}
```

The `exercise` and `duration` fields are required. Duration must be a positive integer. Notes are optional.

#### List workouts with pagination

`GET /workouts?page=1&per_page=10`

The endpoint returns the authenticated user's workouts and pagination information, including the current page, page size, total records, and number of pages.

#### Retrieve a workout

`GET /workouts/1`

Replace `1` with the workout's ID.

#### Update a workout

`PATCH /workouts/1`

Example request:

```json
{
  "duration": 20,
  "notes": "Four sets"
}
```

Only the fields being changed need to be included.

#### Delete a workout

`DELETE /workouts/1`

Replace `1` with the workout's ID.

Users can only access and modify their own workouts. A workout belonging to another user is returned as not found.

## Example Usage with cURL

### 1. Register a user

```bash
curl -X POST http://127.0.0.1:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"password123"}'
```

### 2. Log in and save the JWT

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"password123"}' \
  | python -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')
```

### 3. View the current user

```bash
curl http://127.0.0.1:5000/me \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Create a workout

```bash
curl -X POST http://127.0.0.1:5000/workouts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"exercise":"Running","duration":30,"notes":"Morning run"}'
```

### 5. List workouts

```bash
curl "http://127.0.0.1:5000/workouts?page=1&per_page=10" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Run the tests

From the project root, execute:

```bash
python -m pytest -v
```

## Project Structure

```text
workout-tracker-backend/
├── app.py
├── auth.py
├── workouts.py
├── models.py
├── extensions.py
├── seed.py
├── migrations/
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_workouts.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Error Responses

The API uses HTTP status codes to indicate the result of a request. Examples include:

- `200 OK` — Request successful.
- `201 Created` — Resource created successfully.
- `400 Bad Request` — Invalid input.
- `401 Unauthorized` — Missing or invalid authentication token, or invalid login credentials.
- `404 Not Found` — Resource not found or not accessible to the authenticated user.
- `409 Conflict` — Username already exists.

## Security Notes

- Passwords are stored as hashes rather than plaintext.
- Protected routes require a valid JWT access token.
- Users cannot access another user's workouts.
- Configure a strong JWT secret through an environment variable before deployment.
- Do not commit credentials or production secrets to version control.