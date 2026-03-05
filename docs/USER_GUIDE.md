# Driving School App - User Guide

This guide is for administrators and staff who will be managing the driving school test system.

## Table of Contents

1. [Accessing the Admin Panel](#accessing-the-admin-panel)
2. [Configuring School Settings](#configuring-school-settings)
3. [Managing Exams](#managing-exams)
4. [Managing Questions](#managing-questions)
5. [Importing/Exporting Questions](#importingexporting-questions)
6. [Viewing Student Records](#viewing-student-records)
7. [Viewing Exam Reports](#viewing-exam-reports)
8. [Creating Student Users](#creating-student-users)

---

## Accessing the Admin Panel

1. Log in to your Frappe/ERPNext site as an administrator
2. Navigate to the **Driving School** module from the sidebar or search bar
3. You will see the following doctypes:
   - Driving School Settings
   - Driving School Exam
   - Driving School Question
   - Driving School Student
   - Exam Attempt
   - Exam Answer

---

## Configuring School Settings

The Driving School Settings is where you configure your school's branding and exam rules.

### To Access Settings:

1. Go to **Driving School > Driving School Settings**
2. Or search for "Driving School Settings" in the search bar

### Settings Options:

| Field | Description |
|-------|-------------|
| **School Name** | Your driving school's name (displayed on the test portal) |
| **Logo** | Upload your school logo (displayed on the test portal header) |
| **Exam Duration** | Time limit for each exam in minutes (default: 10) |
| **Questions Per Exam** | Number of questions shown per exam (default: 25) |
| **Pass Mark** | Minimum percentage required to pass (default: 67%) |
| **Allow Retake** | Whether students can retake exams |
| **Retake Wait Days** | Days a student must wait before retaking (0 = immediate retake allowed) |

### Saving Settings:

Click **Save** after making changes. Settings take effect immediately for new exam sessions.

---

## Managing Exams

Exams are collections of questions that students can take.

### Creating a New Exam:

1. Go to **Driving School > Driving School Exam**
2. Click **+ Add Driving School Exam**
3. Fill in the details:
   - **Exam Name**: A descriptive name (e.g., "Learner's License Theory Test")
   - **Description**: Optional description of the exam
   - **Is Active**: Check to make the exam available to students
4. Click **Save**

### Adding Questions to an Exam:

1. Open the exam you want to edit
2. Scroll to the **Questions** table
3. Click **Add Row**
4. Select questions from the dropdown (questions must be created first)
5. Click **Save**

### Activating/Deactivating Exams:

- Check/uncheck the **Is Active** checkbox
- Only active exams appear in the student test portal

---

## Managing Questions

Questions are the individual test items with multiple choice answers.

### Creating a New Question:

1. Go to **Driving School > Driving School Question**
2. Click **+ Add Driving School Question**
3. Fill in the details:

| Field | Description |
|-------|-------------|
| **Question Text** | The question being asked |
| **Question Image** | Optional image for the question |
| **Option 1** | First answer choice (text) |
| **Option 1 Image** | Optional image for first choice |
| **Option 2** | Second answer choice (text) |
| **Option 2 Image** | Optional image for second choice |
| **Option 3** | Third answer choice (text) |
| **Option 3 Image** | Optional image for third choice |
| **Correct Option** | Select which option (1, 2, or 3) is correct |

4. Click **Save**

### Tips for Questions:

- You can use text-only, image-only, or both for questions and options
- Images are useful for road signs, traffic situations, etc.
- Keep question text clear and concise

---

## Importing/Exporting Questions

### Exporting Questions:

1. Go to **Driving School > Driving School Question**
2. Click **Menu (...)** > **Export**
3. Select the format (Excel or CSV)
4. Choose which fields to export
5. Click **Export**

### Importing Questions:

1. Go to **Driving School > Driving School Question**
2. Click **Menu (...)** > **Import**
3. Download the template first to see the required format
4. Fill in your questions in the template
5. Upload the completed file
6. Review and click **Import**

### Import Template Format:

| Column | Required | Description |
|--------|----------|-------------|
| question_text | Yes | The question text |
| question_image | No | Path to question image |
| option_1 | Yes | First option text |
| option_1_image | No | Path to option 1 image |
| option_2 | Yes | Second option text |
| option_2_image | No | Path to option 2 image |
| option_3 | Yes | Third option text |
| option_3_image | No | Path to option 3 image |
| correct_option | Yes | 1, 2, or 3 |

---

## Viewing Student Records

### Accessing Student List:

1. Go to **Driving School > Driving School Student**
2. You'll see all registered students with:
   - First Name
   - Last Name
   - ID Number
   - License Class
   - Registration Date

### Student Details:

Click on any student to view:
- Personal information
- Exam history (linked Exam Attempts)

### Searching Students:

Use the search bar or filters to find students by:
- Name
- ID Number
- License Class

---

## Viewing Exam Reports

### Exam Attempts Report:

1. Go to **Driving School > Exam Attempt**
2. You'll see all exam attempts with:
   - Student Name
   - Exam Name
   - Score
   - Percentage
   - Pass/Fail Status
   - Date Taken

### Filtering Reports:

Use filters to narrow down results:
- **By Student**: See all attempts by a specific student
- **By Exam**: See all attempts for a specific exam
- **By Status**: Filter by Passed/Failed
- **By Date**: Filter by date range

### Viewing Attempt Details:

1. Click on any Exam Attempt
2. You'll see:
   - Overall score and percentage
   - Time taken
   - Individual question answers in the **Answers** table
   - Each answer shows: Question, Selected Option, Correct Option, Is Correct

### Exporting Reports:

1. Apply your desired filters
2. Click **Menu (...)** > **Export**
3. Choose format (Excel/CSV)
4. Click **Export**

### Creating Custom Reports:

For advanced reporting:
1. Go to **Build > Report Builder**
2. Select the Exam Attempt or Exam Answer doctype
3. Add your desired columns and filters
4. Save the report for future use

---

## Creating Student Users

If you want students to log in with Frappe accounts (instead of guest access):

### Creating a Student User:

1. Go to **Setup > User**
2. Click **+ Add User**
3. Fill in:
   - Email
   - First Name
   - Last Name
4. In the **Roles** section, add the role: **Driving School Student**
5. Click **Save**
6. The user will receive a password setup email

### What Student Users Get:

- Automatic redirect to the test portal on login
- Their exam history is linked to their user account
- Access restricted to the test portal only (no desk access)

---

## Troubleshooting

### Students Can't Access Test Portal

- Verify the URL: `/student-test` or `/assets/driving_school/driving-test/index.html`
- Check that at least one exam is marked as **Active**
- Ensure questions are added to the active exam

### Images Not Displaying

- Ensure images are uploaded through the Frappe file manager
- Check file permissions in Frappe

### Exam Not Appearing for Students

- Verify the exam's **Is Active** checkbox is checked
- Ensure the exam has questions assigned

### Student Can't Retake Exam

- Check the **Allow Retake** setting
- Check the **Retake Wait Days** setting
- Verify the waiting period has elapsed

---

## Support

For technical issues, please contact your system administrator or refer to the Technical Guide.
