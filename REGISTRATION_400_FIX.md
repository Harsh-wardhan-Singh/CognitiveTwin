# Registration 400 Bad Request - Fix Guide

## Problem
When trying to register, you're getting a `400 Bad Request` error. This is a validation error from the backend.

## Root Causes & Solutions

### 1. **Email Format Validation**
The backend uses `EmailStr` which has strict validation rules.

**Valid Examples:**
- `student@example.com`
- `john.doe@university.edu`
- `test.user+tag@domain.com`

**Invalid Examples:**
- `student` (missing @domain)
- `@example.com` (missing username)
- `student@.com` (missing domain name)
- `student@domain` (missing TLD)
- `student exam@example.com` (spaces)

### 2. **Role Value Must Be Exact**
The role must be exactly one of these values (case-sensitive, lowercase):
- `student`
- `teacher`

NOT:
- `Student`
- `Teacher`
- `admin`
- `user`

### 3. **Password Requirements**
- Minimum length: 6 characters
- All characters allowed (numbers, letters, special chars)

### 4. **Email Already Exists**
If you try to register with an email that's already in the database, you'll get a 400 error with message:
```
Email already registered
```

## How to Debug

### Option A: Using Browser DevTools

1. Open your browser's Developer Tools (F12)
2. Go to the **Network** tab
3. Try to register an account
4. Find the `register` POST request
5. Click on it and view the **Response** tab
6. You should see detailed error information like:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "details": [
    {
      "field": "email",
      "message": "value is not a valid email address: (...details...)",
      "type": "value_error.email"
    }
  ]
}
```

### Option B: Using curl

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@test.com","password":"password123","role":"student"}'
```

### Option C: Using Python

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "email": "student@test.com",
        "password": "password123",
        "role": "student"
    }
)

print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))
```

## Testing Checklist

- [ ] Backend is running on `http://localhost:8000`
- [ ] Email contains @ and a valid domain
- [ ] Email doesn't have spaces or special characters (except . + -)
- [ ] Role is exactly "student" or "teacher" (lowercase)
- [ ] Password is at least 6 characters
- [ ] Password and confirm password match
- [ ] Using a NEW email (not already registered)

## Example Valid Registration Data

```json
{
  "email": "alice.smith@example.com",
  "password": "MySecurePass123!",
  "role": "student"
}
```

## Next Registration Attempts Should Work

After our fixes, you should see:

1. **Success**: Page shows "Account created! Redirecting..." and you're logged in
2. **Validation Error**: Error message displays the specific field and issue (e.g., "email: value is not a valid email address")
3. **Email Exists**: Error message shows "Email already registered"

## Start Backend

Make sure backend is running:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Should show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

