# Quiz Platform - Database ERD

**Last Updated:** November 4, 2025  
**Source:** Inspected from PostgreSQL `quizdb` database

## Entity Relationship Diagram

```
┌──────────────────────────────┐
│   quiz_category              │  Quiz topics (Python, Math, Web Dev)
├──────────────────────────────┤
│ 🔑 id (BIGINT, PK)           │
│    name (VARCHAR 100)        │
│    description (TEXT)        │
│    created_at (TIMESTAMPTZ)  │
└──────────────────────────────┘
          │
          │ 1:Many
          ▼
┌──────────────────────────────┐
│   quiz_question              │  Quiz questions with soft delete
├──────────────────────────────┤
│ 🔑 id (BIGINT, PK)           │
│ 🔗 category_id (BIGINT, FK)  │ → quiz_category.id
│    text (TEXT)               │
│    question_type (VARCHAR 10)│  'single' or 'multiple'
│    is_deleted (BOOLEAN)      │
│    deleted_at (TIMESTAMPTZ)  │  Nullable
│    created_at (TIMESTAMPTZ)  │
│    updated_at (TIMESTAMPTZ)  │
└──────────────────────────────┘
          │
          │ 1:Many
          ▼
┌──────────────────────────────┐
│   quiz_option                │  Answer choices (A, B, C, D)
├──────────────────────────────┤
│ 🔑 id (BIGINT, PK)           │
│ 🔗 question_id (BIGINT, FK)  │ → quiz_question.id
│    text (VARCHAR 500)        │
│    is_correct (BOOLEAN)      │  True/False
└──────────────────────────────┘


┌──────────────────────────────┐
│   auth_user                  │  Django built-in user table
├──────────────────────────────┤
│ 🔑 id (INTEGER, PK)          │
│    username (VARCHAR 150)    │
│    password (VARCHAR 128)    │  Hashed
│    email (VARCHAR 254)       │
│    first_name (VARCHAR 150)  │
│    last_name (VARCHAR 150)   │
│    is_active (BOOLEAN)       │
│    is_staff (BOOLEAN)        │
│    is_superuser (BOOLEAN)    │
│    date_joined (TIMESTAMPTZ) │
│    last_login (TIMESTAMPTZ)  │
└──────────────────────────────┘
          │
          │ 1:Many
          ▼
┌──────────────────────────────┐
│   quiz_quizattempt           │  User's quiz session
├──────────────────────────────┤
│ 🔑 id (BIGINT, PK)           │
│ 🔗 user_id (INTEGER, FK)     │ → auth_user.id
│ 🔗 category_id (BIGINT, FK)  │ → quiz_category.id
│    total_questions (INT)     │
│    passing_score (INT)       │  Required score (e.g., 70)
│    time_limit (INT)          │  Minutes
│    score (INT)               │  Nullable, calculated %
│    passed (BOOLEAN)          │
│    started_at (TIMESTAMPTZ)  │
│    completed_at (TIMESTAMPTZ)│  Nullable
└──────────────────────────────┘
          │
          │ 1:Many
          ▼
┌──────────────────────────────┐
│   quiz_answer                │  User's response per question
├──────────────────────────────┤
│ 🔑 id (BIGINT, PK)           │
│ 🔗 attempt_id (BIGINT, FK)   │ → quiz_quizattempt.id
│ 🔗 question_id (BIGINT, FK)  │ → quiz_question.id
│    is_flagged (BOOLEAN)      │  Mark for review
│    answered_at (TIMESTAMPTZ) │
│                              │
│ ⚠️  Constraint: UNIQUE       │
│     (attempt_id, question_id)│
└──────────────────────────────┘
          │
          │ Many:Many
          ▼
┌──────────────────────────────┐
│ quiz_answer_selected_options │  Junction table
├──────────────────────────────┤
│ 🔑 id (BIGINT, PK)           │
│ 🔗 answer_id (BIGINT, FK)    │ → quiz_answer.id
│ 🔗 option_id (BIGINT, FK)    │ → quiz_option.id
└──────────────────────────────┘
```

## Foreign Key Relationships

| From Table                     | Column        | References            | Description                           |
| ------------------------------ | ------------- | --------------------- | ------------------------------------- |
| `quiz_question`                | `category_id` | `quiz_category.id`    | Each question belongs to one category |
| `quiz_option`                  | `question_id` | `quiz_question.id`    | Each option belongs to one question   |
| `quiz_quizattempt`             | `user_id`     | `auth_user.id`        | Each attempt is made by one user      |
| `quiz_quizattempt`             | `category_id` | `quiz_category.id`    | Each attempt is for one category      |
| `quiz_answer`                  | `attempt_id`  | `quiz_quizattempt.id` | Each answer belongs to one attempt    |
| `quiz_answer`                  | `question_id` | `quiz_question.id`    | Each answer is for one question       |
| `quiz_answer_selected_options` | `answer_id`   | `quiz_answer.id`      | Links answer to selected options      |
| `quiz_answer_selected_options` | `option_id`   | `quiz_option.id`      | Links selected option to answer       |

## Complete Table Details

### 1. quiz_category

| Column        | Type         | Nullable | Key | Description          |
| ------------- | ------------ | -------- | --- | -------------------- |
| `id`          | BIGINT       | NO       | PK  | Unique identifier    |
| `name`        | VARCHAR(100) | NO       |     | Category name        |
| `description` | TEXT         | NO       |     | Category description |
| `created_at`  | TIMESTAMPTZ  | NO       |     | Creation timestamp   |

### 2. quiz_question

| Column          | Type        | Nullable | Key | Description            |
| --------------- | ----------- | -------- | --- | ---------------------- |
| `id`            | BIGINT      | NO       | PK  | Unique identifier      |
| `category_id`   | BIGINT      | NO       | FK  | Links to quiz_category |
| `text`          | TEXT        | NO       |     | Question text          |
| `question_type` | VARCHAR(10) | NO       |     | 'single' or 'multiple' |
| `is_deleted`    | BOOLEAN     | NO       |     | Soft delete flag       |
| `deleted_at`    | TIMESTAMPTZ | YES      |     | When deleted           |
| `created_at`    | TIMESTAMPTZ | NO       |     | Creation timestamp     |
| `updated_at`    | TIMESTAMPTZ | NO       |     | Last update timestamp  |

### 3. quiz_option

| Column        | Type         | Nullable | Key | Description            |
| ------------- | ------------ | -------- | --- | ---------------------- |
| `id`          | BIGINT       | NO       | PK  | Unique identifier      |
| `question_id` | BIGINT       | NO       | FK  | Links to quiz_question |
| `text`        | VARCHAR(500) | NO       |     | Option text            |
| `is_correct`  | BOOLEAN      | NO       |     | True if correct answer |

### 4. auth_user (Django built-in)

| Column         | Type         | Nullable | Key    | Description           |
| -------------- | ------------ | -------- | ------ | --------------------- |
| `id`           | INTEGER      | NO       | PK     | Unique identifier     |
| `username`     | VARCHAR(150) | NO       | UNIQUE | Login username        |
| `password`     | VARCHAR(128) | NO       |        | Hashed password       |
| `email`        | VARCHAR(254) | YES      |        | User email            |
| `first_name`   | VARCHAR(150) | YES      |        | First name            |
| `last_name`    | VARCHAR(150) | YES      |        | Last name             |
| `is_active`    | BOOLEAN      | NO       |        | Account active status |
| `is_staff`     | BOOLEAN      | NO       |        | Staff access          |
| `is_superuser` | BOOLEAN      | NO       |        | Admin access          |
| `date_joined`  | TIMESTAMPTZ  | NO       |        | Registration date     |
| `last_login`   | TIMESTAMPTZ  | YES      |        | Last login time       |

### 5. quiz_quizattempt

| Column            | Type        | Nullable | Key | Description            |
| ----------------- | ----------- | -------- | --- | ---------------------- |
| `id`              | BIGINT      | NO       | PK  | Unique identifier      |
| `user_id`         | INTEGER     | NO       | FK  | Links to auth_user     |
| `category_id`     | BIGINT      | NO       | FK  | Links to quiz_category |
| `total_questions` | INTEGER     | NO       |     | Number of questions    |
| `passing_score`   | INTEGER     | NO       |     | Required score to pass |
| `time_limit`      | INTEGER     | NO       |     | Time limit in minutes  |
| `score`           | INTEGER     | YES      |     | Calculated score %     |
| `passed`          | BOOLEAN     | NO       |     | Pass/fail status       |
| `started_at`      | TIMESTAMPTZ | NO       |     | When quiz started      |
| `completed_at`    | TIMESTAMPTZ | YES      |     | When quiz completed    |

### 6. quiz_answer

| Column        | Type        | Nullable | Key | Description               |
| ------------- | ----------- | -------- | --- | ------------------------- |
| `id`          | BIGINT      | NO       | PK  | Unique identifier         |
| `attempt_id`  | BIGINT      | NO       | FK  | Links to quiz_quizattempt |
| `question_id` | BIGINT      | NO       | FK  | Links to quiz_question    |
| `is_flagged`  | BOOLEAN     | NO       |     | Mark for review           |
| `answered_at` | TIMESTAMPTZ | NO       |     | When answered             |

**Unique Constraint:** (attempt_id, question_id) - One answer per question per attempt

### 7. quiz_answer_selected_options (Junction Table)

| Column      | Type   | Nullable | Key | Description          |
| ----------- | ------ | -------- | --- | -------------------- |
| `id`        | BIGINT | NO       | PK  | Unique identifier    |
| `answer_id` | BIGINT | NO       | FK  | Links to quiz_answer |
| `option_id` | BIGINT | NO       | FK  | Links to quiz_option |

## Database Statistics

**Total Tables:** 16 (6 quiz tables + 10 Django system tables)

**Quiz-specific Tables:**

- `quiz_category` - 3 records (Python, Web Dev, General Knowledge)
- `quiz_question` - 12 records
- `quiz_option` - Multiple options per question
- `quiz_quizattempt` - User quiz sessions
- `quiz_answer` - User responses
- `quiz_answer_selected_options` - Selected options

## Legend

- 🔑 **PK** = Primary Key (unique identifier)
- 🔗 **FK** = Foreign Key (links to another table)
- **1:Many** = One-to-many relationship
- **Many:Many** = Many-to-many relationship (via junction table)
- **TIMESTAMPTZ** = Timestamp with timezone
- **VARCHAR(n)** = Variable character field with max length
- **TEXT** = Unlimited text field
- **BOOLEAN** = True/False field
- **INTEGER/BIGINT** = Whole number field

## How to View This in DBeaver

1. Connect to `quizdb` database
2. Expand: **quizdb** → **Databases** → **quizdb** → **Schemas** → **public** → **Tables**
3. Right-click any table → **View Data** to see records
4. Right-click any table → **View Diagram** to see relationships visually
5. Use SQL Editor to run queries on this data

## Sample Queries

### View all categories with question count

```sql
SELECT c.name, COUNT(q.id) as question_count
FROM quiz_category c
LEFT JOIN quiz_question q ON c.id = q.category_id
WHERE q.is_deleted = false
GROUP BY c.id, c.name
ORDER BY c.name;
```

### View recent quiz attempts

```sql
SELECT
    u.username,
    c.name as category,
    qa.score,
    qa.passed,
    qa.started_at,
    qa.completed_at
FROM quiz_quizattempt qa
JOIN auth_user u ON qa.user_id = u.id
JOIN quiz_category c ON qa.category_id = c.id
ORDER BY qa.started_at DESC
LIMIT 10;
```

### View questions with their options

```sql
SELECT
    q.text as question,
    o.text as option,
    o.is_correct
FROM quiz_question q
JOIN quiz_option o ON q.id = o.question_id
WHERE q.is_deleted = false
ORDER BY q.id, o.id;
```
