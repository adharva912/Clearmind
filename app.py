from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import google.generativeai as genai
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------
# CONFIGURATION
# -------------------------------
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# -------------------------------
# DATA STORAGE FILES
# -------------------------------
USERS_FILE = 'users.json'
USER_DATA_DIR = 'user_data'

# Ensure directories exist
os.makedirs(USER_DATA_DIR, exist_ok=True)

# -------------------------------
# PASTE YOUR GEMINI API KEY HERE
# -------------------------------
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Choose model
model = genai.GenerativeModel("gemini-1.5-flash")

# Helper function for AI responses
def generate_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}. Using fallback response."

# -------------------------------
# UTILITY FUNCTIONS
# -------------------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_user_data_file(user_id):
    return os.path.join(USER_DATA_DIR, f'{user_id}.json')

def load_user_data(user_id):
    data_file = get_user_data_file(user_id)
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {
        'explanations': [],
        'reflections': [],
        'revisions': [],
        'problems': []
    }

def save_user_data(user_id, data):
    data_file = get_user_data_file(user_id)
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

def get_current_user_id():
    return session.get('user_id')

def require_login():
    if 'user_id' not in session:
        flash('Please login to access this feature')
        return redirect(url_for('login'))
    return None

# -------------------------------
# AUTHENTICATION ROUTES
# -------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        users = load_users()
        if email in users:
            flash('Email already registered')
            return redirect(url_for('register'))

        user_id = str(len(users) + 1)
        users[email] = {
            'id': user_id,
            'email': email,
            'password_hash': generate_password_hash(password, method='pbkdf2:sha256'),
            'created_at': datetime.utcnow().isoformat()
        }
        save_users(users)

        # Initialize user data
        save_user_data(user_id, {
            'explanations': [],
            'reflections': [],
            'revisions': [],
            'problems': []
        })

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        users = load_users()
        user = users.get(email)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --------------------------------
# HOME ROUTE
# --------------------------------
@app.route("/")
def home():
    if 'user_id' in session:
        return render_template("index.html")
    else:
        return render_template("landing.html")
 
 
# --------------------------------
# AI EXPLANATION ENGINE
# --------------------------------
@app.route("/explain", methods=["POST"])
def explain_topic():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Please login first"})

    data = request.json
    topic = data.get("topic")

    prompt = f"Explain the topic '{topic}' in a clear, educational way suitable for students. Include key concepts, simple explanation, real examples, and why it matters. Structure your response with headings."
    result = generate_ai_response(prompt)

    return jsonify({
        "status": "success",
        "explanation": result
    }) 
 
 
# --------------------------------
# PROBLEM GENERATOR
# --------------------------------
@app.route("/generate_problem", methods=["POST"])
def generate_problem():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Please login first"})

    data = request.json
    topic = data.get("topic")

    prompt = f"Generate a real-world problem that applies the concept of '{topic}'. Include a problem statement, background information, challenge question, and considerations. Structure it educationally."
    result = generate_ai_response(prompt)

    # Save to user data
    user_id = session['user_id']
    user_data = load_user_data(user_id)
    user_data['problems'].append({
        'topic': topic,
        'problem': result,
        'created_at': datetime.utcnow().isoformat()
    })
    save_user_data(user_id, user_data)

    return jsonify({
        "status": "success",
        "problem": result
    }) 
 
 
# --------------------------------
# STUDENT EXPLANATION EVALUATION
# --------------------------------
@app.route("/evaluate_explanation", methods=["POST"])
def evaluate_explanation():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Please login first"})

    data = request.json
    topic = data.get("topic")
    student_explanation = data.get("explanation")

    prompt = f"Evaluate this student explanation of '{topic}':\n\n{student_explanation}\n\nProvide constructive feedback including strengths, areas for improvement, suggestions, and a score out of 100."
    result = generate_ai_response(prompt)

    # Save to user data
    user_id = session['user_id']
    user_data = load_user_data(user_id)
    user_data['explanations'].append({
        'topic': topic,
        'explanation': student_explanation,
        'ai_feedback': result,
        'created_at': datetime.utcnow().isoformat()
    })
    save_user_data(user_id, user_data)

    return jsonify({
        "status": "success",
        "feedback": result
    }) 
 
 
# --------------------------------
# REFLECTION ANALYZER
# --------------------------------
@app.route("/analyze_reflection", methods=["POST"])
def analyze_reflection():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Please login first"})

    data = request.json
    reflection = data.get("reflection")

    prompt = f"Analyze this learning reflection:\n\n{reflection}\n\nIdentify positive patterns, thinking patterns, potential biases, and suggestions for growth."
    result = generate_ai_response(prompt)

    # Save to user data
    user_id = session['user_id']
    user_data = load_user_data(user_id)
    user_data['reflections'].append({
        'reflection': reflection,
        'ai_analysis': result,
        'created_at': datetime.utcnow().isoformat()
    })
    save_user_data(user_id, user_data)

    return jsonify({
        "status": "success",
        "analysis": result
    }) 
 
 
# --------------------------------
# REVISION CHECK
# --------------------------------
@app.route("/revision_check", methods=["POST"])
def revision_check():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Please login first"})

    data = request.json
    topic = data.get("topic")
    revision_text = data.get("revision")

    prompt = f"Analyze this revision text for '{topic}':\n\n{revision_text}\n\nEvaluate what is remembered correctly, what needs review, missing elements, and provide study recommendations with a confidence level."
    result = generate_ai_response(prompt)

    # Save to user data
    user_id = session['user_id']
    user_data = load_user_data(user_id)
    user_data['revisions'].append({
        'topic': topic,
        'revision_text': revision_text,
        'ai_feedback': result,
        'created_at': datetime.utcnow().isoformat()
    })
    save_user_data(user_id, user_data)

    return jsonify({
        "status": "success",
        "revision_feedback": result
    }) 
 
 
# --------------------------------
# MASTERY SCORE CALCULATOR
# --------------------------------
@app.route("/calculate_mastery", methods=["POST"])
def calculate_mastery():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Please login first"})

    # Get user's recent activity scores
    user_id = session['user_id']
    user_data = load_user_data(user_id)

    # Calculate average scores based on user activity
    explanation_score = min(100, len(user_data['explanations']) * 10)  # More explanations = higher score
    problem_score = min(100, len(user_data['problems']) * 10)  # More problems = higher score
    revision_score = min(100, len(user_data['revisions']) * 15)  # More revisions = higher score
    reflection_score = min(100, len(user_data['reflections']) * 20)  # More reflections = higher score

    mastery_score = (
        explanation_score * 0.25 +
        problem_score * 0.35 +
        revision_score * 0.25 +
        reflection_score * 0.15
    )

    return jsonify({
        "status": "success",
        "mastery_score": mastery_score
    }) 
 
 
# --------------------------------
# START SERVER
# --------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)