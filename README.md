# Driving School

A Frappe application for managing driving school tests and examinations.

## Features

- **Admin Management**
  - Configure school settings (name, logo, exam duration, pass mark)
  - Create and manage exams
  - Add questions with text or image options
  - Import/export questions via JSON

- **Student Test Taking**
  - Student self-registration with ID number
  - Timed examinations (auto-submit on timeout)
  - Randomized questions from question pool
  - Immediate results with pass/fail status

## Installation

```bash
# Install the app
bench get-app driving_school

# Install on your site
bench --site your-site install-app driving_school

# Run migrations
bench --site your-site migrate
```

## Usage

### Admin
Access the Frappe desk to manage:
- Driving School Settings (Single DocType)
- Driving School Exam
- Driving School Question
- View Exam Attempts and Results

### Students
Access the test portal at: `/driving-test`

Students enter their details and can take available exams.

## License

MIT
