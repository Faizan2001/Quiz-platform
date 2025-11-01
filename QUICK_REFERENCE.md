# Quick Reference - Daily Commands

## Starting Development

```bash
# 1. Open terminal in your project folder
cd ~/Desktop/Quiz-platform

# 2. Activate virtual environment (MUST DO FIRST!)
source venv/bin/activate

# You should see (venv) before your terminal prompt

# 3. Start the server
python manage.py runserver

# 4. Open browser to http://127.0.0.1:8000
```

## Stopping Development

```bash
# 1. Stop server (in terminal where it's running)
CTRL + C

# 2. Deactivate virtual environment
deactivate
```

## Database Changes

When you edit `models.py`:

```bash
# 1. Create migration file
python manage.py makemigrations

# 2. Apply to database
python manage.py migrate

# That's it! Your database is updated
```

## User Management

```bash
# Create superuser (admin)
python manage.py createsuperuser

# Create regular user (in shell)
python manage.py shell
```

Then in Python shell:

```python
from django.contrib.auth.models import User
User.objects.create_user('username', 'email@example.com', 'password')
exit()
```

## Debugging

```bash
# Check for errors
python manage.py check

# See database tables
python manage.py dbshell
\dt  # List tables
\q   # Quit

# Python shell with Django
python manage.py shell
```

Example shell commands:

```python
from quiz.models import *

# See all categories
Category.objects.all()

# Count questions
Question.objects.count()

# Get specific question
q = Question.objects.get(id=1)
print(q.text)

# See options for a question
q.options.all()
```

## File Locations

```
Important files you'll edit:

quiz/models.py          ← Database structure
quiz/views.py           ← Page logic
quiz/urls.py            ← URL routing
quiz/admin.py           ← Admin interface
quiz/templates/quiz/    ← HTML files
quizplatform/settings.py ← Project settings
```

## Making Changes

### Change Page Text

Edit files in `quiz/templates/quiz/`

### Change Colors/Styles

Edit `quiz/templates/quiz/base.html` (look for `<style>` section)

### Add New Page

1. Add function in `views.py`
2. Add URL in `urls.py`
3. Create template in `templates/quiz/`

### Add Database Field

1. Edit `models.py`
2. Run `makemigrations`
3. Run `migrate`

## Demo Data & Accounts

```bash
# Load demo categories, questions, and demo user
python manage.py loaddemo

# Demo user (after loaddemo):
#   Username: demo
#   Password: demo123

# Create an admin user for /admin
python manage.py createsuperuser
```

## Emergency Fixes

### Server won't start?

```bash
source venv/bin/activate  # Did you forget this?
python manage.py check    # What's the error?
```

### Database error?

- Using SQLite (default in `.env`): no service needed. Ensure `USE_SQLITE=True`.
- Using PostgreSQL: ensure the service is running.

```bash
sudo systemctl status postgresql  # Is it running?
sudo systemctl start postgresql   # Start it
```

### Made a mistake?

```bash
git status              # See what changed
git diff               # See exact changes
git checkout filename  # Undo changes to file
```

### Reset demo data (deletes all data!)

```bash
python manage.py flush
python manage.py loaddemo
```

## Adding Python Packages

```bash
# Activate venv first!
source venv/bin/activate

# Install package
pip install package-name

# Save to requirements (so others can install)
pip freeze > requirements.txt
```

## Git Commands

```bash
# See what changed
git status

# Save changes
git add .
git commit -m "Description of what you changed"

# See history
git log --oneline

# Create backup branch
git branch backup-$(date +%Y%m%d)
```

## Useful Django Shell Commands

```bash
python manage.py shell
```

```python
# Import everything
from quiz.models import *
from django.contrib.auth.models import User

# Count stuff
Question.objects.count()
User.objects.count()
QuizAttempt.objects.filter(passed=True).count()

# Create stuff
cat = Category.objects.create(name="Math", description="Math questions")
q = Question.objects.create(text="What is 1+1?", category=cat)
Option.objects.create(question=q, text="2", is_correct=True)

# Delete stuff
q = Question.objects.get(id=1)
q.delete()  # Soft delete (is_deleted=True)

# Get user's quiz history
user = User.objects.get(username='demo')
user.quiz_attempts.all()

# Exit
exit()
```

## Backup Database

```bash
# Backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

## URLs Cheatsheet

```
http://127.0.0.1:8000/                    → Redirects to dashboard
http://127.0.0.1:8000/admin/              → Admin panel
http://127.0.0.1:8000/quiz/login/         → Login page
http://127.0.0.1:8000/quiz/dashboard/     → Main dashboard
http://127.0.0.1:8000/quiz/start-quiz/1/  → Start quiz for category ID 1
```

## Daily Workflow

```bash
# Morning
cd ~/Desktop/Quiz-platform
source venv/bin/activate
python manage.py runserver

# Work on your changes...
# Edit files, test in browser

# Before leaving
# Save your work
git add .
git commit -m "What you did today"

# Stop server
CTRL + C
deactivate
```

## When Help is Needed

1. Error message - Google it with "django" prefix
2. Django docs: https://docs.djangoproject.com/
3. HTMX docs: https://htmx.org/
4. Stack Overflow: Search for similar errors

## Learning Resources

- Django Tutorial: https://docs.djangoproject.com/en/5.1/intro/tutorial01/
- HTMX Examples: https://htmx.org/examples/
- Python Reference: https://docs.python.org/3/

---

Reference guide for common Django development tasks.
