from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
import base64
import uuid
import time
from flask import make_response
from flask_bcrypt import Bcrypt, generate_password_hash




app = Flask(__name__)
app.secret_key = '(X)gi==A=~j0zX_`=@/XL"FPps\apO'  # Update with your secret key
bcrypt = Bcrypt(app)

TASKS_FOLDER = 'user_tasks'


if not os.path.exists(TASKS_FOLDER):
    os.makedirs(TASKS_FOLDER)

# Define security questions
SECURITY_QUESTIONS = [
    "What was the name of your first pet?",
    "In what city were you born?",
    "What is your favorite movie?",
    "What is your mother's maiden name?",
    "What is the name of your favorite teacher?",
    "What was the make and model of your first car?",
    "What is the name of your favorite childhood friend?",
    "What is the birthplace of your father?",
    "What is the title of your favorite book?",
    "In what year did you graduate from high school?"
]


# Load user data from users.json
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}


# Save user data to users.json
def save_users(users):
    try:
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print(f"Error saving users: {str(e)}")




# Function to verify user's identity by answering security question
def verify_user(username, password, security_answer):
    users = load_users()
    if username in users:
        user_data = users[username]
        if bcrypt.check_password_hash(user_data['password'], password) and user_data['security_answer'] == security_answer:
            return True
    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        task_file_name = generate_task_file_name(username)
        task_file_path = os.path.join(TASKS_FOLDER, task_file_name)

        tasks = []

        if os.path.exists(task_file_path):
            with open(task_file_path, 'r') as f:
                tasks = json.load(f)

        return render_template('dashboard.html', tasks=tasks, task=None,username=username)  
        # Pass task=None if it's not available, and the username to 
        # Render to the template file
    else:
        flash('You must log in to access the dashboard.')
        return redirect(url_for('login'))

    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordconf = request.form['passwordconf']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']

        users = load_users()

        # Ensure users is loaded
        if not users:
            users = {}
        # Check if the username already exists
        if password != passwordconf:
            flash('Password and confirmation dont match.')
            return redirect(url_for('register'))
        
        if passwordconf != passwordconf:
            flash('Password and confirmation dont match.')
            return redirect(url_for('register'))
        
        if username in users:
            flash('Username already exists.')
            return redirect(url_for('register'))
        else:
            # Hash the password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Save only necessary information
            users[username] = {
                'password': hashed_password,
                'security_question': security_question,
                'security_answer': security_answer
            }
            save_users(users)
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))

    return render_template('register.html', security_questions=SECURITY_QUESTIONS)


    return render_template('register.html', security_questions=SECURITY_QUESTIONS)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        security_answer = request.form['security_answer']

        if verify_user(username, password, security_answer):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username, password, or security answer. Please try again.')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear
    flash('You have been logged out.')
    return redirect(url_for('index'))


# Function to assign unique IDs to tasks
def assign_task_ids(tasks):
    for task in tasks:
        task['id'] = str(uuid.uuid4())

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' in session:
        username = session['username']
        task_name = request.form['task_name']
        task_description = request.form['task_description']

        task_file_name = generate_task_file_name(username)
        task_file_path = os.path.join(TASKS_FOLDER, task_file_name)

        tasks = []

        if os.path.exists(task_file_path):
            with open(task_file_path, 'r') as f:
                tasks = json.load(f)

        new_task = {'id': str(uuid.uuid4()), 'name': task_name, 'description': task_description, 'completed': False}
        tasks.append(new_task)

        with open(task_file_path, 'w') as f:
            json.dump(tasks, f, indent=2)

        # Redirect to the dashboard after adding the task
        return redirect(url_for('dashboard'))
    else:
        # Return error if user is not logged in
        return jsonify({'error': 'User not logged in'}), 401


@app.route('/edit_task/<task_id>', methods=['POST'])
def edit_task(task_id):
    if 'username' in session:
        username = session['username']
        task_file_name = generate_task_file_name(username)
        task_file_path = os.path.join(TASKS_FOLDER, task_file_name)

        if os.path.exists(task_file_path):
            with open(task_file_path, 'r') as f:
                tasks = json.load(f)

            for task in tasks:
                if task['id'] == task_id:
                    # Update task details
                    task['description'] = request.form.get('description')
                    task['additional_description'] = request.form.get('additional_description')

            # Write the updated tasks back to the file
            with open(task_file_path, 'w') as f:
                json.dump(tasks, f, indent=2)

            return redirect(url_for('task_detail', task_id=task_id))
        else:
            return jsonify({'error': 'Task file not found'}), 404
    else:
        return jsonify({'error': 'User not logged in'}), 401


# app.py
@app.route('/dashboard/task/<task_id>')
def task_detail(task_id):
    if 'username' in session:
        # Retrieve the task details based on the task_id
        task = get_task_by_id(task_id)
        if task:
            return render_template('task_detail.html', task=task)
        else:
            flash('Task not found.')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))



# This line should be indented to be part of the else block
@app.route('/delete_task', methods=['POST'])
def delete_task():
    if 'username' in session:
        username = session['username']
        task_id = request.json.get('taskId')

        task_file_name = generate_task_file_name(username)
        task_file_path = os.path.join(TASKS_FOLDER, task_file_name)

        if os.path.exists(task_file_path):
            with open(task_file_path, 'r') as f:
                tasks = json.load(f)

            # Filter out the task with the given taskId
            filtered_tasks = [task for task in tasks if task['id'] != task_id]

            # Save the updated tasks to the file
            with open(task_file_path, 'w') as f:
                json.dump(filtered_tasks, f, indent=2)

            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'error': 'Task file not found'}), 404
    else:
        return jsonify({'error': 'User not logged in'}), 401
    
# Function to get task details by ID
def get_task_by_id(task_id):
    if 'username' in session:
        username = session['username']
        task_file_name = generate_task_file_name(username)
        task_file_path = os.path.join(TASKS_FOLDER, task_file_name)

        if os.path.exists(task_file_path):
            with open(task_file_path, 'r') as f:
                tasks = json.load(f)

            # Find the task with the given ID
            for task in tasks:
                if task['id'] == task_id:
                    return task

    return None



@app.route('/toggle_task', methods=['POST'])
def toggle_task():
    if 'username' in session:
        username = session['username']
        task_id = request.json.get('taskId')

        task_file_name = generate_task_file_name(username)
        task_file_path = os.path.join(TASKS_FOLDER, task_file_name)

        if os.path.exists(task_file_path):
            with open(task_file_path, 'r') as f:
                tasks = json.load(f)

            for task in tasks:
                if task['id'] == task_id:
                    task['completed'] = not task['completed']

            with open(task_file_path, 'w') as f:
                json.dump(tasks, f, indent=2)

            return jsonify({'message': 'Task toggled successfully'}), 200
        else:
            return jsonify({'error': 'Task file not found'}), 404
    else:
        return jsonify({'error': 'User not logged in'}), 401


# Helper function to generate unique task file name
def generate_task_file_name(username):
    encoded_username = base64.b64encode(username.encode()).decode()
    return f'tasks_{encoded_username}.json'


if __name__ == '__main__':
    app.run(debug=True)
