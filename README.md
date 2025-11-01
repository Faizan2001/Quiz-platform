# Quiz Platform

A Django-based quiz platform with PostgreSQL and HTMX for dynamic interactions. This demo showcases a minimal, stable quiz system with user authentication, multiple-choice questions, and instant result tracking.

## Features

- **User Authentication**: Secure login system
- **Quiz Categories**: Organize questions by topic (Python, Web Development, General Knowledge)
- **Multiple Choice Questions**: Single and multiple-answer support
- **Real-time Interactions**: HTMX-powered dynamic question loading
- **Question Flagging**: Mark questions for review during quiz
- **Instant Results**: Detailed score breakdown and answer review
- **Admin Interface**: Full CRUD operations for quiz content
- **PostgreSQL Database**: Production-ready data storage

## Tech Stack

- **Backend**: Django 5.1+
- **Database**: PostgreSQL
- **Frontend**: Django Templates + HTMX
- **Python**: 3.8+

## Quick Start

If you just want to run it locally without setting up a database, use the SQLite path below. PostgreSQL is optional for local testing.

### Run on Ubuntu (simplest: SQLite, no DB setup)

1) Install Python tools
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip
   ```
2) Get the code and enter the folder
   ```bash
   git clone <your-repo-url>
   cd Quiz-platform
   ```
3) Create and activate a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4) Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
5) Configure environment (uses SQLite by default)
   ```bash
   cp .env.example .env
   # .env already has USE_SQLITE=True for quick local runs
   ```
6) Initialize the app
   ```bash
   python manage.py migrate
   python manage.py loaddemo   # adds demo data and user
   python manage.py createsuperuser  # optional: for /admin
   ```
7) Run the server
   ```bash
   python manage.py runserver
   ```
8) Open in your browser
   - App: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/
      - Demo login: username `demo`, password `demo123`

#### Every Time You Run

- Open a terminal and go to the project folder
- Activate venv:
  - Ubuntu: `source venv/bin/activate`
  - Windows (CMD): `venv\Scripts\activate`
- Start the server: `python manage.py runserver`
- Visit: http://127.0.0.1:8000/
- Stop when done: press `Ctrl+C` in the terminal

#### Occasionally

- After pulling code that changes models: `python manage.py migrate`
- If requirements changed: `pip install -r requirements.txt`
- If you want to refresh demo data:
  - Re-run `python manage.py loaddemo` (it's safe; it won't duplicate questions)
  - To fully reset local data (careful, deletes everything): `python manage.py flush` then `loaddemo`
- If using SQLite: your data lives in `db.sqlite3`. Delete that file to reset everything.

### Run on Windows (simplest: SQLite, no DB setup)

1) Install Python from https://www.python.org/downloads/ and check “Add Python to PATH”.

2) Open Command Prompt and go to the project folder
   ```bat
   cd path\to\Quiz-platform
   ```
3) Create and activate a virtual environment
   ```bat
   py -m venv venv
   venv\Scripts\activate
   ```
4) Install dependencies
   ```bat
   py -m pip install -r requirements.txt
   ```
5) Configure environment (uses SQLite by default)
   ```bat
   copy .env.example .env
   ```
6) Initialize the app
   ```bat
   python manage.py migrate
   python manage.py loaddemo
   python manage.py createsuperuser   REM optional: for /admin
   ```
7) Run the server
   ```bat
   python manage.py runserver
   ```
8) Open in your browser
   - App: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/
   - Demo login: username `demo`, password `demo123`

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip and virtualenv

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Quiz-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

Option A — Quick (use SQLite, no PostgreSQL):

1. Copy env and enable SQLite
   ```bash
   cp .env.example .env
   # ensure USE_SQLITE=True inside .env
   ```
2. Skip to step 4 (Migrations)

Option B — PostgreSQL (recommended for production):

Create a PostgreSQL database and user:

```bash
# Access PostgreSQL
sudo -u postgres psql

# In PostgreSQL shell
CREATE DATABASE quizdb;
CREATE USER quizuser WITH PASSWORD 'your_secure_password';
ALTER ROLE quizuser SET client_encoding TO 'utf8';
ALTER ROLE quizuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE quizuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE quizdb TO quizuser;
\q
```

### 3. Environment Configuration

Copy the example environment file and update with your settings (set `USE_SQLITE=True` to skip PostgreSQL locally):

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-generate-a-new-one
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=quizdb
DB_USER=quizuser
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

**Security Note**: Generate a new SECRET_KEY for production. You can use:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 4. Database Migrations

Apply database migrations to create tables:

```bash
python manage.py migrate
```

### 5. Create Superuser

Create an admin account for the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 6. Load Demo Data

Populate the database with sample questions and a demo user:

```bash
python manage.py loaddemo
```

This creates:

- 3 quiz categories (Python Programming, Web Development, General Knowledge)
- 12 sample questions across all categories
- Demo user account (username: `demo`, password: `demo123`)

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Login Credentials

After loading demo data:

- **Admin Panel**: http://127.0.0.1:8000/admin/
  - Username: Your superuser credentials
- **Quiz Platform**: http://127.0.0.1:8000/
  - Demo User: `demo` / `demo123`

## Project Structure

```
Quiz-platform/
├── quiz/                      # Main quiz application
│   ├── management/
│   │   └── commands/
│   │       └── loaddemo.py   # Demo data loader command
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   └── quiz/
│   ├── admin.py             # Admin interface config
│   ├── models.py            # Database models
│   ├── urls.py              # URL routing
│   └── views.py             # View logic
├── quizplatform/            # Project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # Root URL config
│   └── wsgi.py              # WSGI config
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Usage Guide

### Taking a Quiz

1. Log in at http://127.0.0.1:8000/
2. Select a quiz category from the dashboard
3. Answer questions (checkboxes for multiple choice, radio for single)
4. Use Next/Previous to move between questions
5. Use "Flag for Review" to mark questions to revisit; the review panel shows answered/unanswered/flagged status
6. Submit is only available on the last question
7. View detailed results with correct/incorrect answers

### Managing Content (Admin)

1. Access admin panel at http://127.0.0.1:8000/admin/
2. Log in with superuser credentials
3. Manage:
   - **Categories**: Add/edit quiz topics
   - **Questions**: Create questions with inline options
   - **Options**: Define answer choices (mark correct answers)
   - **Quiz Attempts**: View user quiz history
   - **Answers**: Review individual user responses
   
Notes for demo:
- Users choose a category to start a quiz. Admin changes to categories, questions, and options are reflected immediately.
- CSV upload is not implemented yet; admin adds/edit questions directly via this UI for now.

### Adding New Questions

Via Admin Interface:

1. Go to Questions → Add Question
2. Enter question text and select category
3. Choose question type (single/multiple choice)
4. Add 4 options inline
5. Mark correct answer(s)
6. Save

## Development

### Database Migrations

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating New Admins

```bash
python manage.py createsuperuser
```

### Clearing Demo Data

To reset and reload demo data:

```bash
# Clear all data (careful!)
python manage.py flush

# Reload demo data
python manage.py loaddemo
python manage.py createsuperuser  # Create new admin
```

### Running Tests

```bash
python manage.py test quiz
```

## HTMX Integration

The platform uses HTMX for dynamic interactions without full page reloads:

- **Question Navigation**: Load questions via AJAX
- **Auto-save Answers**: Save selections on change
- **Flag Toggle**: Update review status instantly
- **Review Panel**: Update flagged questions list

HTMX is loaded via CDN in `base.html`. No build step required.

## Minimal Feature Set

This demo includes:

- User authentication and sessions
- Quiz categories
- Single and multiple-choice questions
- Quiz attempts with score tracking
- Question flagging for review
- Dynamic question navigation (HTMX)
- Detailed results page
- Full admin CRUD interface
- PostgreSQL database
- Environment-based configuration

Not included (future enhancements):

- Timer per quiz
- Question explanations
- User profiles and statistics
- Leaderboards
- REST API
- Email notifications

## Security Considerations

- **SECRET_KEY**: Never commit `.env` file. Always use unique secret keys.
- **DEBUG**: Set `DEBUG=False` in production.
- **ALLOWED_HOSTS**: Update with your domain in production.
- **Database Credentials**: Use strong passwords and restrict access.
- **CSRF Protection**: Enabled by default in Django.
- **Password Hashing**: Django uses PBKDF2 by default.

## Troubleshooting

### Database Connection Error

```
django.db.utils.OperationalError: could not connect to server
```

**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql
```

### Import Error: environ

```
ModuleNotFoundError: No module named 'environ'
```

**Solution**: Install dependencies in virtual environment.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Static Files Not Loading

**Solution**: In development, Django serves static files automatically. Ensure `DEBUG=True` in `.env`.

### Migration Errors

```
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Solution**: Clear migrations and rebuild (development only):

```bash
# Delete migration files (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Generate a new `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Use a production-grade web server (Gunicorn + Nginx)
5. Set up SSL/TLS certificates
6. Configure database backups
7. Set up logging and monitoring
8. Use environment variables for all secrets
9. Collect static files: `python manage.py collectstatic`
10. Consider using PostgreSQL connection pooling

## License

This project is a demo/educational resource. 

## Support

For issues or questions:

- Check the troubleshooting section above
- Review Django documentation: https://docs.djangoproject.com/
- Check HTMX documentation: https://htmx.org/

## Contributing

This is a demo project. Feel free to fork and extend with additional features.
