# Development Guide - Understanding the Quiz Platform

## Introduction

This guide explains the concepts and architecture of the quiz platform in clear, professional terms. It covers Django fundamentals, database design, and the application workflow.

## Core Concepts

### Django Framework

Django is a high-level Python web framework that follows the Model-View-Template (MVT) pattern:

- **Model**: Defines data structure and database schema
- **View**: Contains business logic and handles requests
- **Template**: Presents data to users (HTML)

### PostgreSQL Database

PostgreSQL is a relational database management system (RDBMS) that:

- Stores data in structured tables
- Ensures data integrity through constraints
- Supports concurrent access
- Provides transaction safety

### HTMX

HTMX is a library that enables dynamic web interactions through HTML attributes:

- Sends AJAX requests without JavaScript code
- Updates parts of pages without full reload
- Simplifies frontend development

## Application Architecture

### Request-Response Flow

```
User Browser
    ↓
Django URL Router (urls.py)
    ↓
View Function (views.py)
    ↓
Database Query (models.py)
    ↓
PostgreSQL Database
    ↓
Template Rendering (templates/)
    ↓
HTML Response to Browser
```

### Component Interaction

1. **User Action**: User clicks "Start Quiz"
2. **URL Routing**: Django matches `/quiz/start-quiz/1/` to view
3. **View Processing**: `start_quiz()` function executes
4. **Database Query**: Retrieves questions from PostgreSQL
5. **Business Logic**: Randomly selects 10 questions
6. **Database Write**: Creates QuizAttempt and Answer records
7. **Response**: Redirects to quiz taking page
8. **Template Render**: Shows first question

## Database Design

### Entity Relationship

```
Category (1) -----> (Many) Question
Question (1) -----> (Many) Option
User (1) -----> (Many) QuizAttempt
QuizAttempt (1) -----> (Many) Answer
Answer (Many) <-----> (Many) Option (selected)
Question (1) <------ (Many) Answer
```

### Model Definitions

#### Category Model

Represents quiz subjects (Python, Web Development, etc.)

Fields:

- `name`: CharField - Category name
- `description`: TextField - Category description
- `created_at`: DateTimeField - Creation timestamp

#### Question Model

Stores quiz questions

Fields:

- `text`: TextField - Question text
- `category`: ForeignKey - Links to Category
- `question_type`: CharField - 'single' or 'multiple'
- `is_deleted`: BooleanField - Soft delete flag
- `created_at`: DateTimeField - Creation timestamp
- `updated_at`: DateTimeField - Last update timestamp

#### Option Model

Answer choices for questions

Fields:

- `question`: ForeignKey - Links to Question
- `text`: CharField - Option text
- `is_correct`: BooleanField - Whether option is correct

#### QuizAttempt Model

Tracks quiz sessions

Fields:

- `user`: ForeignKey - Links to User
- `category`: ForeignKey - Links to Category
- `total_questions`: IntegerField - Number of questions
- `passing_score`: IntegerField - Required score percentage
- `score`: IntegerField - Achieved score
- `passed`: BooleanField - Pass/fail status
- `started_at`: DateTimeField - Start time
- `completed_at`: DateTimeField - Completion time

#### Answer Model

User's responses to questions

Fields:

- `attempt`: ForeignKey - Links to QuizAttempt
- `question`: ForeignKey - Links to Question
- `selected_options`: ManyToManyField - Selected Option(s)
- `is_flagged`: BooleanField - Flagged for review
- `answered_at`: DateTimeField - Answer timestamp

### Database Operations

#### Object-Relational Mapping (ORM)

Django's ORM translates Python code to SQL:

**Python Code:**

```python
questions = Question.objects.filter(category_id=1)
```

**Generated SQL:**

```sql
SELECT * FROM quiz_question WHERE category_id = 1;
```

**Benefits:**

- Database-agnostic code
- Protection against SQL injection
- Automatic query optimization
- Pythonic syntax

#### Common Query Patterns

**Retrieve all objects:**

```python
categories = Category.objects.all()
```

**Filter objects:**

```python
python_questions = Question.objects.filter(category__name='Python')
```

**Get single object:**

```python
question = Question.objects.get(id=1)
```

**Create object:**

```python
category = Category.objects.create(name='Python', description='...')
```

**Update object:**

```python
category.description = 'Updated description'
category.save()
```

**Delete object (soft delete):**

```python
question.is_deleted = True
question.save()
```

**Relationships:**

```python
# Forward relationship
question.category.name  # Access related category

# Reverse relationship
category.questions.all()  # All questions in category
```

## View Functions

### Purpose

Views handle HTTP requests and return HTTP responses. Each view:

1. Receives request data
2. Performs business logic
3. Queries database
4. Renders template or redirects
5. Returns response

### Implementation Examples

#### Dashboard View

```python
@login_required
def dashboard(request):
    # Query database
    categories = Category.objects.all()
    recent_attempts = QuizAttempt.objects.filter(
        user=request.user,
        completed_at__isnull=False
    ).order_by('-completed_at')[:5]

    # Prepare context
    context = {
        'categories': categories,
        'recent_attempts': recent_attempts,
    }

    # Render template
    return render(request, 'quiz/dashboard.html', context)
```

**Breakdown:**

- `@login_required`: Decorator ensures user is authenticated
- Database queries retrieve categories and attempts
- Context dictionary passes data to template
- `render()` combines template with data

#### Start Quiz View

```python
@login_required
def start_quiz(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Get questions
    all_questions = list(Question.objects.filter(
        category=category,
        is_deleted=False
    ))

    # Random selection
    num_questions = min(10, len(all_questions))
    selected_questions = random.sample(all_questions, num_questions)

    # Create quiz attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        category=category,
        total_questions=num_questions
    )

    # Create answer records
    for question in selected_questions:
        Answer.objects.create(
            attempt=attempt,
            question=question
        )

    return redirect('take_quiz', attempt_id=attempt.id)
```

**Breakdown:**

- `get_object_or_404()`: Returns object or 404 error
- `random.sample()`: Randomly selects questions
- Creates database records for attempt and answers
- Redirects to quiz taking page

## Template System

### Template Inheritance

Base template provides common structure:

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>{% block title %}Quiz Platform{% endblock %}</title>
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>
```

Child template extends base:

```html
<!-- dashboard.html -->
{% extends 'quiz/base.html' %} {% block title %}Dashboard{% endblock %} {% block
content %}
<h1>Available Quizzes</h1>
{% for category in categories %}
<div>{{ category.name }}</div>
{% endfor %} {% endblock %}
```

### Template Tags

**Variables:**

```html
{{ category.name }} {{ user.username }}
```

**Filters:**

```html
{{ attempt.completed_at|date:"M d, Y" }} {{ question.text|truncatewords:20 }}
```

**Control Structures:**

```html
{% if user.is_authenticated %}
<p>Welcome, {{ user.username }}</p>
{% else %}
<a href="{% url 'login' %}">Login</a>
{% endif %} {% for question in questions %}
<p>{{ forloop.counter }}. {{ question.text }}</p>
{% endfor %}
```

**URL Generation:**

```html
<a href="{% url 'start_quiz' category.id %}">Start Quiz</a>
```

## URL Routing

### URL Configuration

**Project-level (`quizplatform/urls.py`):**

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
]
```

**App-level (`quiz/urls.py`):**

```python
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start-quiz/<int:category_id>/', views.start_quiz, name='start_quiz'),
]
```

### URL Pattern Components

```python
path('start-quiz/<int:category_id>/', views.start_quiz, name='start_quiz')
```

- `'start-quiz/<int:category_id>/'`: URL pattern with parameter
- `views.start_quiz`: View function to call
- `name='start_quiz'`: Name for reverse URL lookup

### Dynamic URLs

**In template:**

```html
<a href="{% url 'start_quiz' category.id %}">Start</a>
```

**Generates:**

```html
<a href="/quiz/start-quiz/1/">Start</a>
```

**In views:**

```python
return redirect('quiz_results', attempt_id=attempt.id)
```

## HTMX Integration

### How HTMX Works

HTMX adds attributes to HTML elements that trigger AJAX requests:

```html
<div
  hx-get="/quiz/1/question/5/"
  hx-target="#question-container"
  hx-swap="innerHTML"
>
  Question 5
</div>
```

**Attributes:**

- `hx-get`: URL to fetch
- `hx-target`: Element to update
- `hx-swap`: How to insert content

**User clicks div:**

1. HTMX sends GET request to `/quiz/1/question/5/`
2. Server returns HTML fragment
3. HTMX inserts HTML into `#question-container`
4. No page reload

### Auto-save Implementation

```html
<form
  hx-post="{% url 'question_view' attempt.id answer.id %}"
  hx-trigger="change"
  hx-swap="none"
>
  <input type="radio" name="options" value="1" />
</form>
```

**Behavior:**

- User selects radio button
- `change` event triggers
- HTMX posts form data
- Server saves selection
- No visual change needed (`hx-swap="none"`)

## Admin Interface

### Configuration

```python
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'category', 'question_type')
    list_filter = ('category', 'question_type')
    search_fields = ('text',)
    inlines = [OptionInline]
```

**Features:**

- `list_display`: Columns in list view
- `list_filter`: Sidebar filters
- `search_fields`: Search box fields
- `inlines`: Edit related objects inline

### Inline Admin

```python
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
    fields = ('text', 'is_correct')
```

**Purpose:** Edit options while editing question

## Authentication

### Login Required Decorator

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Only authenticated users can access
    pass
```

**Behavior:**

- Checks if user is authenticated
- Redirects to login page if not
- Calls view if authenticated

### User Object

Available in all views as `request.user`:

```python
current_user = request.user
username = request.user.username
is_staff = request.user.is_staff
```

In templates:

```html
{{ user.username }} {% if user.is_authenticated %}...{% endif %}
```

## Migrations

### Purpose

Migrations track database schema changes:

- Version control for database
- Apply changes incrementally
- Reversible operations

### Workflow

1. **Modify model:**

```python
class Question(models.Model):
    difficulty = models.CharField(max_length=20)  # New field
```

2. **Create migration:**

```bash
python manage.py makemigrations
```

Django creates `quiz/migrations/0002_question_difficulty.py`

3. **Apply migration:**

```bash
python manage.py migrate
```

PostgreSQL table updated with new column

### Migration File

```python
operations = [
    migrations.AddField(
        model_name='question',
        name='difficulty',
        field=models.CharField(max_length=20),
    ),
]
```

## Development Workflow

### Standard Development Cycle

1. **Plan feature:** Define requirements
2. **Update model:** Add/modify fields in `models.py`
3. **Create migration:** `makemigrations`
4. **Apply migration:** `migrate`
5. **Create view:** Add function in `views.py`
6. **Add URL:** Map URL to view in `urls.py`
7. **Create template:** Design HTML in `templates/`
8. **Test:** Verify functionality in browser
9. **Commit:** Save changes with git

### Testing Approach

1. **Manual testing:**

   - Navigate through application
   - Test all user flows
   - Verify data in admin panel

2. **Database verification:**

   ```bash
   python manage.py shell
   ```

   ```python
   Question.objects.count()
   QuizAttempt.objects.filter(passed=True).count()
   ```

3. **Server logs:**
   Monitor terminal for errors while testing

## Best Practices

### Model Design

- Use descriptive field names
- Add help_text for clarity
- Implement `__str__()` method
- Use appropriate field types
- Add database indexes for performance

### View Functions

- Keep views focused (single responsibility)
- Use decorators for common functionality
- Handle errors gracefully
- Validate user input
- Use meaningful variable names

### Templates

- Extend base templates
- Avoid logic in templates
- Use template filters
- Keep templates DRY (Don't Repeat Yourself)

### Security

- Never hardcode passwords
- Validate all user input
- Use CSRF protection (enabled by default)
- Sanitize output (automatic in templates)
- Use `@login_required` for protected views

## Troubleshooting

### Common Issues

**Import errors:**

```
ModuleNotFoundError: No module named 'quiz'
```

Solution: Ensure app is in `INSTALLED_APPS`

**Template not found:**

```
TemplateDoesNotExist: quiz/dashboard.html
```

Solution: Check template path and app registration

**Database errors:**

```
relation "quiz_category" does not exist
```

Solution: Run migrations (`python manage.py migrate`)

**URL not found:**

```
NoReverseMatch: Reverse for 'dashboard' not found
```

Solution: Check URL name in `urls.py`

### Debugging Techniques

1. **Print statements:**

```python
print(f"Categories: {categories.count()}")
```

2. **Django shell:**

```bash
python manage.py shell
```

```python
from quiz.models import *
Question.objects.all()
```

3. **Database shell:**

```bash
python manage.py dbshell
```

```sql
SELECT * FROM quiz_question;
```

4. **Error pages:**
   Django shows detailed errors when `DEBUG = True`

## Summary

The quiz platform demonstrates:

- **Django MVT pattern**: Separation of data, logic, and presentation
- **PostgreSQL integration**: Robust data storage
- **ORM usage**: Database operations in Python
- **Authentication**: User login/logout
- **HTMX**: Dynamic interactions without complex JavaScript
- **Admin interface**: Content management
- **Template inheritance**: Reusable HTML structure

Understanding these concepts enables extending the platform with additional features and maintaining the codebase effectively.
