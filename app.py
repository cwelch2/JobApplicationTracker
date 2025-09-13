from flask import Flask, redirect, render_template, request, flash, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

from datetime import datetime
import os

app = Flask(__name__)


app.secret_key = os.getenv("SECRET_KEY", "your-very-secret-key")


# DATABASE_URL allows switching between SQLite (dev) and MySQL (prod)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",
    "sqlite:///jobs.db"  # fallback for local dev
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# setup flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirect to login page if not authenticated

migrate = Migrate(app, db)


# ----------Models-------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    jobs = db.relationship('Job', backref='owner', lazy=True)

    # helpers for password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)  #job title
    company = db.Column(db.String(100), nullable=False)  #company name
    location = db.Column(db.String(100), nullable=False)  #location
    status = db.Column(db.String(20), nullable=False, default='Applied')  #applcation status 
    archived = db.Column(db.Boolean, default=False)  #is the job archived
    
    link = db.Column(db.String(300), nullable=True)  #link to posting (optional)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Job %r' % self.id


# create tables if they don't exist (for local dev)
with app.app_context():
    db.create_all()

#-----------User Auth-------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # reloads user object from session

# route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        password = request.form['password']

        # check if username exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect('/register')

        # create new user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # auto login the new user
        login_user(user)

        return redirect('/')  # redirect to home page
    return render_template('register.html')

# route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # authenticate user
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')
        else:
            flash("Invalid username or password")
            return redirect('/login')
    return render_template('login.html')

# route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


#-----------Job Routes-------------

# route for home page
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # only fetch user's non-archived jobs
    jobs = Job.query.filter_by(archived=False, user_id=current_user.id).all()
    return render_template('index.html', jobs=jobs)

# route for adding a job
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_job():
    if request.method == 'POST':
        # create job tied to current user
        new_job = Job(
            title=request.form['title'],
            company=request.form['company'],
            location=request.form['location'],
            status=request.form.get('status', 'Applied'),
            link=request.form.get('link', ''),
            owner=current_user  
        )
        db.session.add(new_job)
        db.session.commit()
    return redirect('/')

# route for updating job info
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_job(id):
    # only allow editing jobs owned by the current user
    job = Job.query.filter_by(id=id, owner=current_user).first_or_404()
    if request.method == 'POST':
        job.title = request.form['title']
        job.company = request.form['company']
        job.location = request.form['location']
        job.status = request.form['status']
        job.link = request.form.get('link', '')
        try:
            db.session.commit()
            return redirect(request.referrer)  # stay on same page
        except:
            return "There was a problem editing that job"
    return render_template('update_job.html', job=job)

# route for updating status in table
@app.route('/update-status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    job = Job.query.filter_by(id=id, owner=current_user).first_or_404()
    job.status = request.form['status']
    try:
        db.session.commit()
        return redirect(request.referrer)
    except:
        return "There was a problem updating that job's status"

# route for deleting jobs
@app.route('/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_job(id):
    job = Job.query.filter_by(id=id, owner=current_user).first_or_404()
    try:
        db.session.delete(job)
        db.session.commit()
        return redirect(request.referrer)
    except:
        return "There was a problem deleting that job"


# route to flip archived status
@app.route('/toggle-archive/<int:id>', methods=['POST', 'GET'])
@login_required
def archive_job(id):
    job = Job.query.filter_by(id=id, owner=current_user).first_or_404()
    try:
        job.archived = not job.archived
        db.session.commit()
        return redirect(request.referrer)
    except:
        return "There was an issue archiving that job"

# route to archived jobs
@app.route('/archived')
@login_required
def archived_jobs():
    jobs = Job.query.filter_by(archived=True, user_id=current_user.id).all()
    return render_template('archived.html', jobs=jobs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))


