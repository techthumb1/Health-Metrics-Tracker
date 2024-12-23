from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from .models import db, User, Metrics
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

# Blueprint and login manager initialization
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
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email is missing
        if not email:
            flash('Email is required.')
            return redirect(url_for('main.register'))
        
        # Proceed with registration
        user = User(username=username, email=email)
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

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/results')
@login_required
def results():
    metrics = Metrics.query.filter_by(user_id=current_user.id).order_by(Metrics.date).all()
    metrics_data = [
        {
            'date': metric.date.strftime("%Y-%m-%d"),
            'heart_rate': metric.heart_rate,
            'blood_pressure': metric.blood_pressure,
            'weight': metric.weight
        }
        for metric in metrics
    ]
    return render_template('results.html', metrics_data=metrics_data)

def predict_next_value(data):
    if len(data) < 2:
        return None
    X = np.arange(len(data)).reshape(-1, 1)
    y = np.array(data)
    model = LinearRegression().fit(X, y)
    return model.predict([[len(data)]])[0]

def process_metric(metric, metric_name):
    prediction = predict_next_value(metric) if metric else None
    if prediction:
        metric.append(prediction)
        return prediction
    return None

@main.route('/dashboard')
@login_required
def dashboard():
    metrics = Metrics.query.filter_by(user_id=current_user.id).order_by(Metrics.date).all()

    # Extract metrics
    metric_dict = {
        'dates': [metric.date.strftime("%Y-%m-%d") for metric in metrics],
        'heart_rate': [metric.heart_rate for metric in metrics],
        'systolic': [int(bp.split('/')[0]) for bp in metrics if bp.blood_pressure],
        'diastolic': [int(bp.split('/')[1]) for bp in metrics if bp.blood_pressure],
        'weight': [metric.weight for metric in metrics]
    }

    # Generate predictions
    predictions = {key: process_metric(metric_dict[key], key) for key in metric_dict if key != 'dates'}
    if predictions['heart_rate']:
        metric_dict['dates'].append('Prediction')

    return render_template(
        'dashboard.html',
        metrics=metric_dict,
        predictions=predictions,
        current_year=datetime.now().year
    )

@main.route('/log_metrics', methods=['GET', 'POST'])
@login_required
def log_metrics():
    if request.method == 'POST':
        heart_rate = int(request.form.get('heart_rate'))
        blood_pressure = request.form.get('blood_pressure')
        weight = float(request.form.get('weight'))
        weight_unit = request.form.get('weight_unit')

        if weight_unit == 'kg':
            weight *= 2.20462  # Convert kg to lbs

        new_metric = Metrics(
            user_id=current_user.id,
            heart_rate=heart_rate,
            blood_pressure=blood_pressure,
            weight=weight,
            date=datetime.utcnow()
        )
        db.session.add(new_metric)
        db.session.commit()
        flash('Metrics logged successfully.')
        return redirect(url_for('main.dashboard'))

    return render_template('log_metrics.html')
