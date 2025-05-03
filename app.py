from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, Response
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import traceback 
from datetime import datetime 

app = Flask(__name__)
# # Configure a secret key for session management (required for flash messages)
# # Replace with a real secret key in production
app.config['SECRET_KEY'] = 'your_secret_key_here'


CONTRACTOR_CREDENTIALS_FILE = 'contractors.json'
WORKER_DATA_FILE = 'workers.json'
AVAILABLE_WORKERS_CALLS_FILE = 'available_workers_calls.json' 


def load_contractor_credentials():
    """Loads contractor usernames and HASHED passwords and details from a JSON file."""
    if not os.path.exists(CONTRACTOR_CREDENTIALS_FILE):
        
        with open(CONTRACTOR_CREDENTIALS_FILE, 'w') as f:
            json.dump({}, f) 
        return {}
    try:
        with open(CONTRACTOR_CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        
        print(f"Error decoding JSON from {CONTRACTOR_CREDENTIALS_FILE}. File might be empty or corrupted.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred loading {CONTRACTOR_CREDENTIALS_FILE}: {e}")
        traceback.print_exc()
        return {}


def save_contractor_credentials(credentials):
    """Saves contractor usernames and HASHED passwords and details to a JSON file."""
    try:
        with open(CONTRACTOR_CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials, f, indent=4) # Use indent for readability
    except Exception as e:
        print(f"An unexpected error occurred saving to {CONTRACTOR_CREDENTIALS_FILE}: {e}")
        traceback.print_exc()



def load_worker_data():
    """Loads worker data from a JSON file."""
    if not os.path.exists(WORKER_DATA_FILE):
        
        with open(WORKER_DATA_FILE, 'w') as f:
            json.dump([], f) 
        return []
    try:
        with open(WORKER_DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        
        print(f"Error decoding JSON from {WORKER_DATA_FILE}. File might be empty or corrupted.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred loading {WORKER_DATA_FILE}: {e}")
        traceback.print_exc()
        return []

def save_worker_data(workers):
    """Saves worker data to a JSON file."""
    try:
        with open(WORKER_DATA_FILE, 'w') as f:
            json.dump(workers, f, indent=4) 
    except Exception as e:
        print(f"An unexpected error occurred saving to {WORKER_DATA_FILE}: {e}")
        traceback.print_exc()


def load_available_workers_calls():
    """Loads available worker call data from a JSON file."""
    if not os.path.exists(AVAILABLE_WORKERS_CALLS_FILE):
        
        with open(AVAILABLE_WORKERS_CALLS_FILE, 'w') as f:
            json.dump([], f) 
        return []
    try:
        with open(AVAILABLE_WORKERS_CALLS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        
        print(f"Error decoding JSON from {AVAILABLE_WORKERS_CALLS_FILE}. File might be empty or corrupted.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred loading {AVAILABLE_WORKERS_CALLS_FILE}: {e}")
        traceback.print_exc()
        return []

def save_available_workers_calls(calls):
    """Saves available worker call data to a JSON file."""
    try:
        with open(AVAILABLE_WORKERS_CALLS_FILE, 'w') as f:
            json.dump(calls, f, indent=4) 
    except Exception as e:
        print(f"An unexpected error occurred saving to {AVAILABLE_WORKERS_CALLS_FILE}: {e}")
        traceback.print_exc()


@app.route('/favicon.ico')
def favicon():
    """Handle favicon.ico requests by returning a 404."""
    
    try:
        return send_from_directory(app.static_folder, 'favicon.ico')
    except FileNotFoundError:
        return Response(status=404)


@app.route('/')
def index():
    """Landing Page"""
    try:
        return render_template('index.html', title='JobJunction - Connects Laborers and Contractors')
    except Exception as e:
        print(f"Error rendering index page: {e}")
        traceback.print_exc()
        return "An error occurred loading the homepage.", 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Worker Registration Page"""
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        skills = request.form.get('skills')
        experience = request.form.get('experience')
        phone_number = request.form.get('phone_number')

        if not name or not location or not skills or not phone_number:
            flash('Please fill in all required fields.', 'danger')
            try:
                return render_template('register.html', title='Worker Registration')
            except Exception as e:
                print(f"Error rendering worker registration page after validation error: {e}")
                traceback.print_exc()
                return "An error occurred.", 500


        worker_data = load_worker_data()

        if any(worker.get('phone_number') == phone_number for worker in worker_data):
            flash('A worker with this phone number is already registered.', 'danger')
            try:
                return render_template('register.html', title='Worker Registration')
            except Exception as e:
                print(f"Error rendering worker registration page after duplicate phone error: {e}")
                traceback.print_exc()
                return "An error occurred.", 500

        worker_id = 1
        if worker_data:
             worker_id = max(worker.get('id', 0) for worker in worker_data) + 1


        new_worker = {
            'id': worker_id,
            'name': name,
            'location': location,
            'skills': skills,
            'experience': experience,
            'phone_number': phone_number,
        }

        worker_data.append(new_worker)
        save_worker_data(worker_data)

        flash('Registration successful! You can now give a missed call to mark yourself available.', 'success')
        return redirect(url_for('index'))

    try:
        return render_template('register.html', title='Worker Registration')
    except Exception as e:
        print(f"Error rendering worker registration page (GET): {e}")
        traceback.print_exc()
        return "An error occurred loading the registration page.", 500


@app.route('/contractor-register', methods=['GET', 'POST'])
def contractor_register():
    """Contractor Registration Page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        age = request.form.get('age')
        job_type = request.form.get('job_type')


        contractor_credentials = load_contractor_credentials()

        if username in contractor_credentials:
            flash('Username already exists. Please choose a different one.', 'danger')
            try:
                return render_template('contractor_register.html', title='Contractor Registration')
            except Exception as e:
                print(f"Error rendering contractor registration page after duplicate username error: {e}")
                traceback.print_exc()
                return "An error occurred.", 500

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        contractor_details = {
            'password': hashed_password,
            'name': name,
            'phone_number': phone_number,
            'age': age,
            'job_type': job_type
        }

        contractor_credentials[username] = contractor_details
        save_contractor_credentials(contractor_credentials)

        flash('Contractor registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    try:
        return render_template('contractor_register.html', title='Contractor Registration')
    except Exception as e:
        print(f"Error rendering contractor registration page (GET): {e}")
        traceback.print_exc()
        return "An error occurred loading the contractor registration page.", 500


@app.route('/missed-call', methods=['GET', 'POST'])
def missed_call():
    """Handles missed call API endpoint from Exotel or similar."""
    phone_number = request.form.get('CallerId') or request.args.get('CallerId')
    if not phone_number:
        phone_number = request.form.get('phone_number') or request.args.get('phone_number') 
    if not phone_number:
        phone_number = request.form.get('CallFrom') or request.args.get('CallFrom')
    if not phone_number:
        phone_number = request.form.get('From') or request.args.get('From')

    timestamp_str = request.args.get('CurrentTime') 

    print(f"Received missed call request. Method: {request.method}, Data: {request.form or request.args}")
    print(f"Extracted phone number: {phone_number}")


    if phone_number:
        available_calls_data = load_available_workers_calls()
        worker_data = load_worker_data() 

        print(f"Worker data loaded for check: {worker_data}")

        is_registered_worker = any(worker.get('phone_number') == phone_number for worker in worker_data)

        print(f"Is registered worker: {is_registered_worker}") 


        if is_registered_worker:
            new_call_entry = {
                'phone_number': phone_number,
                'timestamp': timestamp_str if timestamp_str else datetime.now().isoformat()
            }

            available_calls_data.append(new_call_entry)
            save_available_workers_calls(available_calls_data)

            print(f"Received missed call from registered worker: {phone_number}. Recorded as available.")
            return 'Missed call recorded', 200
        else:
            print(f"Received missed call from unregistered number: {phone_number}.")
            return 'Phone number not registered as a worker', 404
    else:
        print("No phone number found in request parameters.")
        return 'No phone number provided', 400

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Contractor Login Page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        contractor_credentials = load_contractor_credentials()

        if username in contractor_credentials and check_password_hash(contractor_credentials[username].get('password'), password):

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    try:
        return render_template('login.html', title='Contractor Login')
    except Exception as e:
        print(f"Error rendering login page: {e}")
        traceback.print_exc()
        return "An error occurred loading the login page.", 500


@app.route('/dashboard')

def dashboard():
    """Contractor Dashboard"""
    available_calls_data = load_available_workers_calls()
    worker_data = load_worker_data()


    available_phone_numbers = {call.get('phone_number') for call in available_calls_data if call.get('phone_number')}


    available_workers = [
        worker for worker in worker_data
        if worker.get('phone_number') in available_phone_numbers
    ]

    try:
        return render_template('dashboard.html', title='Contractor Dashboard', workers=available_workers)
    except Exception as e:
        print(f"Error rendering dashboard page: {e}")
        traceback.print_exc()
        return "An error occurred loading the dashboard.", 500


@app.route('/hire/<int:worker_id>', methods=['POST'])

def hire_worker(worker_id):
    """Handles hiring a worker and sending SMS notification."""
    worker_data = load_worker_data()
    worker_to_hire = None
    for worker in worker_data:
        if worker.get('id') == worker_id:
            worker_to_hire = worker
            break

    if worker_to_hire:

        print(f"Simulating sending SMS to worker: {worker_to_hire.get('name', 'N/A')} ({worker_to_hire.get('phone_number', 'N/A')})")
        flash(f'Notification simulated for worker {worker_to_hire.get("name", "N/A")}.', 'success')

    else:
        flash('Worker not found.', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/how-it-works')
def how_it_works():
    """How It Works Page"""
    try:
        return render_template('how_it_works.html', title='How JobJunction Works')
    except Exception as e:
        print(f"Error rendering how it works page: {e}")
        traceback.print_exc()
        return "An error occurred loading the 'How It Works' page.", 500

@app.errorhandler(404)
def page_not_found(e):
    try:
        return render_template('404.html'), 404
    except Exception as render_error:
        print(f"Error rendering 404.html template: {render_error}")
        traceback.print_exc()
        return "Page not found and the error page could not be rendered.", 404


@app.errorhandler(500)
def internal_server_error(e):
    print(f"An internal server error occurred: {e}")
    traceback.print_exc()
    try:
        return render_template('500.html'), 500
    except Exception as render_error:
        print(f"Error rendering 500.html template: {render_error}")
        traceback.print_exc()
        return "An internal server error occurred and the error page could not be rendered.", 500


if __name__ == '__main__':
    load_contractor_credentials()
    load_worker_data()
    load_available_workers_calls() 
    app.run(debug=True)
