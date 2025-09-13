# Job Application Tracker

A web application to help you track your job applications, statuses, and archive old jobs.

## Features

- User registration and login
- Add, edit, and delete job applications
- Track job status (Applied, Interview, Offer Received, Denied)
- Archive jobs for future reference
- Search/filter jobs
- Responsive UI

## Tech Stack

- Python 3.10+ (Flask)
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Jinja2 templates
- SQLite/MySQL (configurable)
- HTML/CSS/JavaScript

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/cwelch2/JobApplicationTracker.git
   cd JobApplicationTracker
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set environment variables (optional):**
   - `SECRET_KEY`: Flask secret key
   - `DATABASE_URL`: Database URI (defaults to SQLite)
   
    > **For hosting:** When deploying the app, use a `.env` file or your hosting provider’s environment variable settings to securely store `SECRET_KEY` and `DATABASE_URL`.


4. **Run the app:**
   ```sh
   python app.py
   ```
   The app will be available at [http://localhost:8000](http://localhost:8000).

## Database Migrations

- Migrations are managed with Alembic and Flask-Migrate.
- Migration scripts are in the `migrations/` directory.

## Folder Structure

- `app.py`: Main application file
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS)
- `instance/`: Local database (ignored by git)
- `migrations/`: Database migration scripts

## License

MIT License

---

For questions or contributions, visit the [GitHub repository](https://github.com/cwelch2/JobApplicationTracker).