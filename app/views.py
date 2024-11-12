from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from .models import db, User, Metrics
from flask import jsonify
from datetime import datetime

main = Blueprint('main', __name__)
login_manager = LoginManager()
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    flash('Welcome to your Health Metrics Tracker. Please Login.')
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

#@main.route('/log_metrics', methods=['GET', 'POST'])
#@login_required
#def log_metrics():
#    if request.method == 'POST':
#        heart_rate = request.form['heart_rate']
#        blood_pressure = request.form['blood_pressure']
#        weight = request.form['weight']
#        new_metric = Metrics(user_id=current_user.id, heart_rate=heart_rate, blood_pressure=blood_pressure, weight=weight)
#        db.session.add(new_metric)
#        db.session.commit()
#        flash('Metrics logged successfully!', 'Success')
#        return redirect(url_for('main.dashboard'))
#    return render_template('log_metrics.html')


@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/dashboard')
@login_required
def dashboard():
    metrics = Metrics.query.filter_by(user_id=current_user.id).order_by(Metrics.date).all()
    
    metrics_dates = [metric.date.strftime("%Y-%m-%d") for metric in metrics]
    heart_rates = [metric.heart_rate for metric in metrics]
    blood_pressures = [metric.blood_pressure for metric in metrics]
    weights = [metric.weight for metric in metrics]

    return render_template('dashboard.html', 
                           metrics_dates=metrics_dates, 
                           heart_rates=heart_rates, 
                           blood_pressures=blood_pressures, 
                           weights=weights)

# Log Metrics
@main.route('/log_metrics', methods=['GET', 'POST'])
@login_required
def log_metrics():
    if request.method == 'POST':
        # Get the form data
        heart_rate = request.form.get('heart_rate')
        blood_pressure = request.form.get('blood_pressure')
        weight = float(request.form.get('weight'))
        weight_unit = request.form.get('weight_unit')

        # Convert weight to pounds if the unit is in kilograms
        if weight_unit == 'kg':
            weight = weight * 2.20462  # Convert kg to lbs

        # Create a new Metrics entry
        new_metric = Metrics(
            user_id=current_user.id,
            heart_rate=int(heart_rate),
            blood_pressure=blood_pressure,
            weight=weight,
            date=datetime.utcnow()
        )

        # Add and commit to the database
        db.session.add(new_metric)
        db.session.commit()

        flash('Metrics logged successfully.')
        return redirect(url_for('main.dashboard'))

    return render_template('log_metrics.html')