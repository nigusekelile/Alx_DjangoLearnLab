# Authentication Documentation

## Overview
Describe how the project handles user authentication: registration, login/logout, session and token management, password reset, email verification (if implemented), and authorization (view-level permissions). This document explains components, user flows, configuration options, security considerations, and how to test each feature.

---

## Components

- User model
    - Default Django `User` or a custom `AUTH_USER_MODEL`. Document fields used (username/email as identifier), and any custom properties (is_staff, is_active, profile relation).

- Authentication backends
    - Built-in Django backend(s) used. Note any custom backends (e.g., email-based login).

- Views / URLs
    - List endpoints: registration, login, logout, password reset (initiate/confirm), email verification endpoints, profile. Note URL names and expected HTTP methods (GET/POST).

- Forms / Serializers
    - Forms for registration/login/password reset (HTML) or DRF serializers for API endpoints. Document required fields and validation rules.

- Sessions & Tokens
    - Session-based auth (Django sessions) or token-based (JWT, DRF Token). Explain storage and lifetime.

- Email
    - Email backend used for password reset and verification. Note templates and where to find them.

- Permissions & Authorization
    - How view access is restricted (login_required, permission_required, DRF permissions). Note any custom decorators or mixins.

---

## User Interaction / Flows

1. Registration
     - User fills registration form (username/email + password + optional fields).
     - On success: account created (is_active may be False if email verification required). Optional auto-login or redirect to login page.

2. Email verification (if enabled)
     - Registration sends verification email with tokenized link.
     - Following link activates the account.

3. Login
     - User submits identifier (username or email) and password.
     - On success: session cookie set (or token returned for API); redirect to dashboard or `LOGIN_REDIRECT_URL`.

4. Logout
     - User triggers logout endpoint: session cleared (server-side) or token revoked on client.

5. Password reset
     - User requests reset by entering email.
     - System sends reset link with token.
     - User sets new password via token-protected form.

6. Protected resources
     - Access to protected views requires authentication; role-based access enforced with permissions.

---

## Configuration (important settings)
- AUTH_USER_MODEL: document custom user path if present.
- AUTHENTICATION_BACKENDS: list any non-default backends.
- LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
- SESSION_COOKIE_AGE, SESSION_EXPIRE_AT_BROWSER_CLOSE
- EMAIL_BACKEND, DEFAULT_FROM_EMAIL, EMAIL_HOST / related SMTP settings
- If API: DRF settings for authentication classes (SessionAuthentication, TokenAuthentication, JWT settings)

---

## Security Considerations
- Password hashing: Django uses secure hashers by default — do not replace with insecure options.
- Enforce password validators (min length, common password checks).
- Use HTTPS in production; set SECURE_SSL_REDIRECT and cookies to Secure, HttpOnly.
- Rate-limit authentication endpoints to mitigate brute-force attacks.
- Set proper account lockout or throttling if needed.
- Ensure token revocation/rotation for long-lived tokens.

---

## How to Test Each Authentication Feature

A. Manual (browser)
- Registration
    1. Navigate to the registration page.
    2. Submit valid form. Confirm user created in admin or DB.
    3. If verification required, check email (console or configured SMTP) for link and follow it.

- Login
    1. Go to login page.
    2. Submit valid credentials. Confirm redirect and that protected pages are accessible.
    3. Submit invalid credentials; confirm error messages and that no session cookie is set.

- Logout
    1. While logged in, click logout.
    2. Confirm redirect and that protected pages now redirect to login.

- Password reset
    1. Use "Forgot password" page, enter registered email.
    2. Confirm email received with reset link (console or SMTP).
    3. Follow link, set new password, confirm login works with new password.

- Email verification (if present)
    1. Register with email; confirm activation step required.
    2. Open verification email and follow link; confirm account active.

B. API / curl / Postman (if API endpoints exist)
- Registration (POST /api/auth/register)
    - Send JSON body with required fields. Expect 201 and optionally token or 200 with verification message.

- Login (POST /api/auth/login)
    - Send credentials; expect token or session cookie. For session authentication, include credentials and capture Set-Cookie header.

- Token-protected resource
    - Call protected endpoint with Authorization: Token <token> or Bearer <jwt>. Expect 200 on valid token, 401 on invalid.

- Password reset initiation (POST /api/auth/password/reset)
    - Provide email. Confirm response and that reset email is queued/sent.

Example curl (session-based):
    - Login: curl -c cookies.txt -d "username=...&password=..." http://localhost:8000/accounts/login/
    - Access protected: curl -b cookies.txt http://localhost:8000/protected/

Example curl (token-based):
    - Obtain token: curl -X POST -H "Content-Type: application/json" -d '{"username":"u","password":"p"}' http://localhost:8000/api/token/
    - Use token: curl -H "Authorization: Bearer <token>" http://localhost:8000/api/me/

C. Automated tests (Django test client / pytest)
- Unit test ideas:
    - Registration creates user and sets expected fields; if email verification required assert is_active False until verification.
    - Login with valid credentials returns 200 and sets session or returns token.
    - Login with invalid credentials returns 401/403 and does not create a session.
    - Password reset: posting to reset sends email and token can be used to change password.
    - Access control: anonymous cannot access login_required views; authenticated user can.
- Example (pytest + Django test client)
    - Create user in test DB, use client.post(reverse("login"), data=...) and assert response status and session key.

D. Email debugging
- For dev use console backend: EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
- For automated tests use Django’s mail.outbox to inspect messages.

---

## Common Troubleshooting
- "Unable to login but credentials correct": check AUTHENTICATION_BACKENDS and AUTH_USER_MODEL, ensure password hashed via set_password.
- "Password reset email not sent": confirm EMAIL_BACKEND and email templates exist; check logs.
- "Session not persisting": check session middleware order, SESSION_COOKIE settings, and that cookies are sent by client.
- "Token auth failing": ensure token included in Authorization header and correct auth class configured.

---

## Checklist for Reviewers / Maintainers
- Verify AUTH_USER_MODEL and migration status.
- Confirm secure email setup for production.
- Ensure password validators are enabled.
- Review any custom authentication backends for security bugs.
- Confirm tests cover registration, login, logout, password reset, and protected resource access.

---

## Where to look in this project
- Models: app/models.py (custom user or profile)
- Views: app/views.py, accounts/views.py, api/views.py
- URLs: project/urls.py, app/urls.py, accounts/urls.py
- Templates: templates/registration/*.html or templates/accounts/*
- Tests: tests/test_auth.py or similar
- Settings: project/settings.py for auth and email configuration

---

If you want, I can generate example unit tests, CURL examples for each endpoint, or a checklist of settings to add to settings.py.  