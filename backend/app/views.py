from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from .models import db, User, Metrics
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
from flask import render_template, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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

@main.route('/health', methods=['GET'])
def health():
    """
    Simple health check endpoint.
    Returns 200 OK if the server is up.
    """
    return jsonify({"status": "ok"}), 200

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

# In views/main.py or wherever your routes are defined

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

@main.route('/contact', methods=['GET'])
def contact():
    """Render the contact form page"""
    return render_template('contact.html')

@main.route('/handle_contact', methods=['POST'])
def handle_contact():
    """Handle the contact form submission"""
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Add your contact form processing logic here
        # For example, sending email, saving to database, etc.
        
        # Flash success message
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        flash('Sorry, there was an error processing your message.', 'error')
        return redirect(url_for('main.contact'))

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

def safe_split_bp(bp_value):
    """Safely split blood pressure values"""
    try:
        if bp_value and '/' in str(bp_value):
            systolic, diastolic = str(bp_value).split('/')
            return int(systolic), int(diastolic)
        return None, None
    except (ValueError, AttributeError) as e:
        logger.error(f"Error processing blood pressure value: {bp_value}, Error: {str(e)}")
        return None, None

def safe_process_metric(metrics, metric_type):
    """Safely process metrics and handle missing values"""
    if not metrics:
        return []
    try:
        # Remove None values and convert to appropriate type
        return [float(m) for m in metrics if m is not None]
    except (ValueError, TypeError) as e:
        logger.error(f"Error processing {metric_type}: {str(e)}")
        return []

@main.route('/dashboard')
@login_required
def dashboard():
    try:
        # Query metrics
        metrics = Metrics.query.filter_by(user_id=current_user.id).order_by(Metrics.date).all()
        
        # Initialize metric dictionary
        metrics_data = {
            'dates': [],
            'heart_rate': [],
            'systolic': [],
            'diastolic': [],
            'weight': []
        }
        
        # Process metrics
        for metric in metrics:
            if metric.date:
                metrics_data['dates'].append(metric.date.strftime("%Y-%m-%d"))
            
            metrics_data['heart_rate'].append(metric.heart_rate if hasattr(metric, 'heart_rate') else None)
            
            if hasattr(metric, 'blood_pressure') and metric.blood_pressure:
                try:
                    sys, dia = metric.blood_pressure.split('/')
                    metrics_data['systolic'].append(float(sys))
                    metrics_data['diastolic'].append(float(dia))
                except (ValueError, AttributeError):
                    metrics_data['systolic'].append(None)
                    metrics_data['diastolic'].append(None)
            
            metrics_data['weight'].append(metric.weight if hasattr(metric, 'weight') else None)
        
        # Clean None values
        for key in metrics_data:
            if key != 'dates':
                metrics_data[key] = [x for x in metrics_data[key] if x is not None]
        
        # Generate predictions
        predictions = {}
        for key in metrics_data:
            if key != 'dates' and metrics_data[key]:
                try:
                    pred = process_metric(metrics_data[key], key)
                    predictions[key] = [pred] if pred is not None else []
                except Exception as e:
                    print(f"Prediction error for {key}: {str(e)}")
                    predictions[key] = []
        
        return render_template(
            'dashboard.html',
            metrics=metrics_data,
            predictions=predictions,
            current_year=datetime.now().year
        )
        
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return render_template(
            'error.html',
            error="Unable to load dashboard data. Please try again later.",
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
