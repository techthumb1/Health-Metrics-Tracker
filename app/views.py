from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from .models import db, User, Metrics
from flask import jsonify
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np


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

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/results')
def results():
    # Assuming data is similar to the previous contact route
    metrics = Metrics.query.filter_by(user_id=current_user.id).order_by(Metrics.date).all()
    
    metrics_data = [
        (
            metric.date.strftime("%Y-%m-%d"),
            float(metric.heart_rate) if metric.heart_rate is not None else None,
            metric.blood_pressure,
            float(metric.weight) if metric.weight is not None else None
        )
        for metric in metrics
    ]
    return render_template('results.html', metrics_data=metrics_data)

@main.route('/handle_results', methods=["POST"])
def handle_results():
    # Placeholder for handling form data on the results page
    # Process form data here
    return redirect(url_for('main.results'))

def predict_next_value(data):
    if len(data) < 2:
        return None  # Not enough data for prediction
    X = np.array(range(len(data))).reshape(-1, 1)
    y = np.array(data)
    model = LinearRegression()
    model.fit(X, y)
    next_x = np.array([[len(data)]])
    return model.predict(next_x)[0]

@main.route('/dashboard')
@login_required
def dashboard():
    metrics = Metrics.query.filter_by(user_id=current_user.id).order_by(Metrics.date).all()

    metrics_dates = [metric.date.strftime("%Y-%m-%d") for metric in metrics] if metrics else []
    heart_rates = [float(metric.heart_rate) for metric in metrics] if metrics else []
    systolic_data = [int(metric.blood_pressure.split('/')[0]) for metric in metrics if metric.blood_pressure] if metrics else []
    diastolic_data = [int(metric.blood_pressure.split('/')[1]) for metric in metrics if metric.blood_pressure] if metrics else []
    weights = [float(metric.weight) for metric in metrics] if metrics else []
    sleep_quality = [int(metric.sleep_quality) for metric in metrics] if metrics else []
    hydration = [float(metric.hydration) for metric in metrics] if metrics else []
    activity_level = [float(metric.activity_level) for metric in metrics] if metrics else []
    blood_glucose = [float(metric.blood_glucose) for metric in metrics] if metrics else []
    oxygen_saturation = [float(metric.oxygen_saturation) for metric in metrics] if metrics else []
    cholesterol = [float(metric.cholesterol) for metric in metrics] if metrics else []
    # Additonal metrics can be added here

    # Generate predictions if data is available
    if heart_rates:
        predicted_heart_rate = float(predict_next_value(heart_rates))
        heart_rates.append(predicted_heart_rate)
        metrics_dates.append('Prediction')
    if systolic_data:
        predicted_systolic = float(predict_next_value(systolic_data))
        systolic_data.append(predicted_systolic)
    if diastolic_data:
        predicted_diastolic = float(predict_next_value(diastolic_data))
        diastolic_data.append(predicted_diastolic)
    if weights:
        predicted_weight = float(predict_next_value(weights))
        weights.append(predicted_weight)
    if sleep_quality:
        predicted_sleep_quality = float(predict_next_value(sleep_quality))
        sleep_quality.append(predicted_sleep_quality)
    if hydration:
        predicted_hydration = float(predict_next_value(hydration))
        hydration.append(predicted_hydration)
    if activity_level:
        predicted_activity_level = float(predict_next_value(activity_level))
        activity_level.append(predicted_activity_level)
    if blood_glucose:
        predicted_blood_glucose = float(predict_next_value(blood_glucose))
        blood_glucose.append(predicted_blood_glucose)
    if oxygen_saturation:
        predicted_oxygen_saturation = float(predict_next_value(oxygen_saturation))
        oxygen_saturation.append(predicted_oxygen_saturation)
    if cholesterol:
        predicted_cholesterol = float(predict_next_value(cholesterol))
        cholesterol.append(predicted_cholesterol)

    current_year = datetime.now().year
    
    # Pass the data to the template
    return render_template('dashboard.html', 
                           metrics_dates=metrics_dates, 
                           heart_rates=heart_rates, 
                           systolic_data=systolic_data, 
                           diastolic_data=diastolic_data, 
                           weights=weights,
                           sleep_quality=sleep_quality,
                           hydration=hydration,
                           activity_level=activity_level,
                           blood_glucose=blood_glucose,
                           oxygen_saturation=oxygen_saturation,
                           cholesterol=cholesterol,
                           current_year=current_year)

# Advanced Metrics Dashboard
@main.route('/advanced_dashboard')
@login_required
def advanced_dashboard():
    # Advaced metrics will require blood tests (lipid panel,  etc.)
    metrics = Metrics.query.filter_by(user_id=current_user.id).order_by(Metrics.date).all()



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