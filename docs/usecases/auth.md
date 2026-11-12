# Use cases: authentication and users

## UC-01 Register

- **Actor:** Guest
- **Precondition:** not logged in.
- **Flow:**
    1. Guest opens Register and enters username, email, full name and password twice.
    2. System validates the input.
    3. System creates a user with role `owner` and `is_active: true`.
    4. System shows a success message and opens Login.
- **Exceptions:**
    - Username or email already used: `409`, form shows which one.
    - Invalid input (short password, bad email, passwords differ): `422`, form shows the field.
- **Realized by:** `POST /auth/register`

## UC-02 Log in

- **Actor:** Guest
- **Precondition:** has an active account.
- **Flow:**
    1. Guest enters username and password.
    2. System checks them and returns a token.
    3. UI loads the current user and shows the pages allowed for the role.
- **Exceptions:**
    - Wrong username, wrong password or deactivated account: `401` with one generic message.
- **Realized by:** `POST /auth/login`, `GET /auth/me`

## UC-03 Log out

- **Actor:** any user
- **Precondition:** logged in.
- **Flow:**
    1. User clicks Log out.
    2. UI deletes the token from the session and opens Login.
- **Exceptions:** none. The token is not revoked on the server; it expires on its own. See [Authentication](../architecture/auth.md).
- **Realized by:** frontend only.

## UC-04 Switch language

- **Actor:** any user, also Guest
- **Precondition:** none.
- **Flow:**
    1. User picks EN or SR in the sidebar.
    2. UI reloads labels from the matching `i18n` file and sends `lang` with every API call.
- **Exceptions:** text without a Serbian version is shown in English.
- **Realized by:** `lang` query parameter on read endpoints.

## UC-05 Manage users and workshops

- **Actor:** Admin
- **Precondition:** logged in as admin.
- **Flow:**
    1. Admin opens Users and workshops and sees all users with role and status.
    2. Admin changes a role, deactivates or reactivates a user.
    3. For a mechanic, admin picks the workshop. System replaces the mechanic's `works_at` edge.
    4. Admin creates or edits a workshop (name, city, address, coordinates).
- **Exceptions:**
    - Admin tries to deactivate or demote himself: `409`, so the system never ends up without an admin.
    - Workshop assigned to a user who is not a mechanic: `409`.
- **Realized by:** `GET /users`, `PATCH /users/{key}`, `PUT /users/{key}/workshop`, `POST/PUT /workshops`
