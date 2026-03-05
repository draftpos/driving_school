# Driving School App - Technical Guide

This guide covers installation, configuration, and technical details for system administrators and developers.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Post-Installation Setup](#post-installation-setup)
4. [App Architecture](#app-architecture)
5. [API Reference](#api-reference)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [Updating the App](#updating-the-app)
9. [Uninstallation](#uninstallation)

---

## Prerequisites

- Frappe Framework v14 or v15
- ERPNext (optional, but recommended)
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+ or MySQL 8.0+
- Redis

---

## Installation

### Step 1: Clone the App

```bash
cd /path/to/frappe-bench

# Clone without building (recommended)
bench get-app --skip-assets https://github.com/draftpos/driving_school.git
```

### Step 2: Add to apps.txt

**Important:** The `bench get-app` command may not automatically add the app to `apps.txt`. You must verify and add it manually if needed.

```bash
# Check if driving_school is in apps.txt
cat sites/apps.txt

# If NOT present, add it manually using a text editor:
nano sites/apps.txt
```

Add `driving_school` on a new line at the end of the file:

```
frappe
erpnext
... (other apps)
driving_school
```

Save and exit (Ctrl+X, then Y, then Enter in nano).

**Note:** Do NOT use `echo "driving_school" >> sites/apps.txt` as it may not add a proper line break and can corrupt the file.

### Step 3: Build Assets

```bash
bench build --app driving_school
```

### Step 4: Install on Site

```bash
bench --site YOUR_SITE_NAME install-app driving_school
```

Replace `YOUR_SITE_NAME` with your actual site name (e.g., `mysite.local` or `erp.mycompany.com`).

### Step 5: Run Migrations

```bash
bench --site YOUR_SITE_NAME migrate
```

### Step 6: Restart Services

For development:
```bash
bench restart
```

For production:
```bash
sudo supervisorctl restart all
```

### Step 7: Clear Cache (Optional but Recommended)

```bash
bench --site YOUR_SITE_NAME clear-cache
```

---

## Post-Installation Setup

### Verify Installation

1. Log in to your site as Administrator
2. Search for "Driving School Settings" in the search bar
3. If it opens, the app is installed correctly

### Initial Configuration

1. Go to **Driving School Settings**
2. Set your school name and logo
3. Configure exam parameters (duration, pass mark, etc.)
4. Save

### Create Your First Exam

1. Create questions: **Driving School > Driving School Question**
2. Create an exam: **Driving School > Driving School Exam**
3. Add questions to the exam
4. Set the exam as **Active**

### Test the Student Portal

Access the student test portal at:
- Primary URL: `https://your-site.com/student-test`
- Direct URL: `https://your-site.com/assets/driving_school/driving-test/index.html`

---

## App Architecture

### Directory Structure

```
driving_school/
├── driving_school/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # Login redirect handler
│   │   ├── files.py         # Private file serving for guests
│   │   └── student.py       # Student/exam API endpoints
│   ├── driving_school/
│   │   ├── doctype/
│   │   │   ├── driving_school_exam/
│   │   │   ├── driving_school_question/
│   │   │   ├── driving_school_settings/
│   │   │   ├── driving_school_student/
│   │   │   ├── exam_answer/
│   │   │   └── exam_attempt/
│   ├── public/
│   │   ├── css/
│   │   │   └── driving_school.css
│   │   ├── driving-test/
│   │   │   └── index.html    # React-based student portal
│   │   └── js/
│   │       └── driving_school.js
│   ├── www/
│   │   └── student-test.html # Redirect page for /student-test URL
│   ├── hooks.py              # App hooks configuration
│   ├── install.py            # Post-install setup
│   └── modules.txt
├── docs/
│   ├── USER_GUIDE.md
│   └── TECHNICAL_GUIDE.md
├── pyproject.toml
└── README.md
```

### DocTypes

| DocType | Purpose |
|---------|---------|
| **Driving School Settings** | Single doctype for app configuration |
| **Driving School Exam** | Exam definitions with linked questions |
| **Driving School Question** | Question bank with options and images |
| **Driving School Student** | Student registration records |
| **Exam Attempt** | Records of exam attempts with scores |
| **Exam Answer** | Individual answers (child table of Exam Attempt) |

### Hooks

Key hooks configured in `hooks.py`:

```python
# Role-based home page redirect
role_home_page = {
    "Driving School Student": "/student-test"
}

# Login event handler
on_login = "driving_school.api.auth.on_login"

# Fixtures (exported with app)
fixtures = [
    {"doctype": "Role", "filters": [["name", "in", ["Driving School Student"]]]},
    {"doctype": "Role Profile", "filters": [["name", "in", ["Driving School Student"]]]}
]

# Post-install setup
after_install = "driving_school.install.after_install"
```

---

## API Reference

All APIs are whitelisted for guest access to support the public test portal.

### GET /api/method/driving_school.api.student.get_settings

Returns public school settings.

**Response:**
```json
{
  "message": {
    "school_name": "My Driving School",
    "logo": "/files/logo.png",
    "exam_duration": 10,
    "pass_mark": 67,
    "questions_per_exam": 25,
    "allow_retake": 1,
    "retake_wait_days": 0
  }
}
```

### GET /api/method/driving_school.api.student.get_exams

Returns list of active exams.

**Parameters:**
- `student_id` (optional): Filter by student ID to check retake eligibility

**Response:**
```json
{
  "message": [
    {
      "name": "EXAM-001",
      "exam_name": "Learner's License Test",
      "description": "Theory test for learner's license"
    }
  ]
}
```

### POST /api/method/driving_school.api.student.register_student

Registers a new student or retrieves existing one.

**Parameters:**
- `first_name`: Student's first name
- `last_name`: Student's last name
- `id_number`: National ID number
- `license_class`: License class applying for

**Response:**
```json
{
  "message": {
    "student_id": "STU-00001",
    "first_name": "John",
    "last_name": "Doe",
    "id_number": "12345678",
    "license_class": "Class 4"
  }
}
```

### GET /api/method/driving_school.api.student.get_exam_questions

Gets randomized questions for an exam.

**Parameters:**
- `exam_id`: The exam document name

**Response:**
```json
{
  "message": [
    {
      "name": "QST-00001",
      "question_text": "What does this sign mean?",
      "question_image": "/private/files/sign.png",
      "option_1": "Stop",
      "option_1_image": null,
      "option_2": "Yield",
      "option_2_image": null,
      "option_3": "Go",
      "option_3_image": null
    }
  ]
}
```

### POST /api/method/driving_school.api.student.submit_exam

Submits exam answers and returns results.

**Parameters:**
- `student_id`: Student document name
- `exam_id`: Exam document name
- `answers`: JSON array of answers `[{"question": "QST-001", "selected_option": 1}, ...]`
- `time_taken`: Time taken in seconds

**Response:**
```json
{
  "message": {
    "attempt_id": "ATT-00001",
    "score": 20,
    "total": 25,
    "percentage": 80.0,
    "passed": true,
    "pass_mark": 67
  }
}
```

### GET /api/method/driving_school.api.files.get_file

Serves private files for driving school content (images).

**Parameters:**
- `file_url`: The private file URL (e.g., `/private/files/image.png`)

**Response:** Binary file content with appropriate MIME type.

---

## Customization

### Changing Theme Colors

Edit the CSS variables in `/driving_school/public/driving-test/index.html`:

```css
:root {
    --primary-color: #7a2e90;    /* Main purple */
    --primary-dark: #5c2270;     /* Darker purple */
    --purple-color: #7a2e90;
    --purple-light: #9b4db0;
}
```

After changes:
```bash
bench build --app driving_school
```

### Adding Custom Fields

Use Frappe's Customize Form feature:
1. Go to **Customize Form**
2. Select the doctype (e.g., Driving School Student)
3. Add your custom fields
4. Save

### Modifying the Student Portal

The student portal is a React application located at:
`/driving_school/public/driving-test/index.html`

It uses inline Babel transpilation for simplicity. For major changes:
1. Edit the HTML file
2. Rebuild: `bench build --app driving_school`
3. Clear cache: `bench --site YOUR_SITE clear-cache`

---

## Troubleshooting

### Build Fails with "paths[0]" Error

**Cause:** Empty `public/js` or `public/css` folders, or app not in `apps.txt`.

**Solution:**
1. Verify `driving_school` is in `sites/apps.txt`
2. Ensure placeholder files exist in `public/js/` and `public/css/`
3. Rebuild: `bench build --app driving_school`

### 403 Forbidden on Images

**Cause:** Private files can't be accessed by guests.

**Solution:** The app includes a file proxy API. Ensure images are being loaded through:
`/api/method/driving_school.api.files.get_file?file_url=...`

### CSRF Token Error on API Calls

**Cause:** POST requests require CSRF token.

**Solution:** Read operations use GET method (no CSRF needed). Write operations (register, submit) must include the CSRF token from cookies.

### Student Portal Shows "Failed to Load"

**Cause:** API endpoint issues or missing configuration.

**Solutions:**
1. Check browser console for errors
2. Verify Driving School Settings exists
3. Check Redis is running: `redis-cli ping`
4. Check site error logs: `bench --site YOUR_SITE show-logs`

### Role Redirect Not Working

**Cause:** Cache or hook issues.

**Solutions:**
1. Clear cache: `bench --site YOUR_SITE clear-cache`
2. Verify role assignment: User must have "Driving School Student" role
3. Check `hooks.py` has correct `role_home_page` configuration

### Exam Questions Not Randomizing

**Cause:** The `get_exam_questions` API randomizes questions.

**Solution:** This is handled server-side using `ORDER BY RAND()`. If seeing same order, it might be browser caching - try hard refresh.

---

## Updating the App

### From GitHub

```bash
cd /path/to/frappe-bench

# Pull latest changes
cd apps/driving_school
git pull origin main
cd ../..

# Rebuild and migrate
bench build --app driving_school
bench --site YOUR_SITE_NAME migrate

# Restart
sudo supervisorctl restart all  # Production
# OR
bench restart  # Development
```

### Clear Cache After Update

```bash
bench --site YOUR_SITE_NAME clear-cache
```

---

## Uninstallation

### Step 1: Uninstall from Site

```bash
bench --site YOUR_SITE_NAME uninstall-app driving_school
```

### Step 2: Remove from apps.txt

Edit `sites/apps.txt` and remove the `driving_school` line.

### Step 3: Remove App Files

```bash
bench remove-app driving_school
```

### Step 4: Restart

```bash
sudo supervisorctl restart all  # Production
# OR
bench restart  # Development
```

---

## Security Considerations

1. **Guest API Access:** The student portal APIs allow guest access. Ensure your server has rate limiting configured.

2. **File Access:** The file proxy only serves files attached to Driving School doctypes, preventing unauthorized file access.

3. **Student Data:** Student records contain personal information (ID numbers). Ensure proper access controls and data protection compliance.

4. **HTTPS:** Always use HTTPS in production to protect student data in transit.

---

## Support

- **GitHub Issues:** https://github.com/draftpos/driving_school/issues
- **Frappe Forum:** https://discuss.frappe.io
