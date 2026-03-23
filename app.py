from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
# import google.generativeai as genai  # Temporarily disabled due to Python 3.14.3 compatibility
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
# genai.configure(api_key=GEMINI_API_KEY)

# Choose model
# model = genai.GenerativeModel("gemini-2.5-flash")

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

    # Mock response for now
    result = f"""
    Here's a clear explanation of {topic}:

    **Key Concepts:**
    - This is a fundamental concept in the field
    - It involves understanding the basic principles
    - Applications are widespread in real-world scenarios

    **Simple Explanation:**
    {topic} refers to the process or system that helps us understand how things work in a particular domain.

    **Real Example:**
    Consider how we use {topic} in everyday life - it helps us make better decisions and solve problems more effectively.

    **Why it matters:**
    Understanding {topic} gives you a foundation for learning more advanced concepts in this field.
    """

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

    # Mock problem generation
    result = f"""
    **Real-World Problem: Applying {topic} in Environmental Science**

    **Problem Statement:**
    A coastal city is experiencing rapid sea-level rise due to climate change. The city needs to develop a comprehensive plan to protect its infrastructure and population.

    **Background:**
    - Sea levels are rising at an average of 3.3mm per year globally
    - Coastal cities worldwide face similar challenges
    - Economic costs of inaction are estimated in billions of dollars

    **Challenge Question:**
    How can principles of {topic} be applied to design sustainable coastal protection systems that balance environmental, economic, and social factors?

    **Consider:**
    - Engineering solutions (sea walls, levees)
    - Natural approaches (mangrove restoration, beach nourishment)
    - Community planning and evacuation strategies
    - Long-term sustainability vs. short-term costs
    """

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

    # Mock AI feedback
    result = f"""
    **Evaluation of your explanation of {topic}:**

    **Strengths:**
    - You provided a clear structure
    - Good attempt at explaining the concept
    - Shows understanding of basic principles

    **Areas for improvement:**
    - Could include more specific examples
    - Consider adding mathematical relationships if applicable
    - Try to connect to real-world applications

    **Suggestions:**
    - Review the fundamental definitions
    - Practice explaining to someone else
    - Look for additional examples online

    **Score: 75/100** - Good foundation, needs more depth.
    """

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

    # Mock reflection analysis
    result = f"""
    **Analysis of Your Learning Reflection:**

    **Positive Patterns Identified:**
    - You're actively engaging with the material
    - Showing metacognitive awareness
    - Willing to identify areas for improvement

    **Thinking Patterns:**
    - Analytical approach to problem-solving
    - Good self-assessment skills
    - Focus on practical applications

    **Potential Biases to Watch For:**
    - Confirmation bias in interpreting results
    - Overconfidence in familiar areas
    - Anchoring to initial hypotheses

    **Suggestions for Growth:**
    - Try different problem-solving approaches
    - Seek feedback from peers regularly
    - Practice explaining concepts to others
    - Keep a learning journal for long-term patterns

    **Overall Assessment:** You're developing strong learning habits. Continue building on these foundations!
    """

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

    # Mock revision feedback
    result = f"""
    **Revision Analysis for {topic}:**

    **What you remembered correctly:**
    - Core concepts are well understood
    - Key relationships identified
    - Good grasp of fundamental principles

    **Important concepts to review:**
    - Some technical details need reinforcement
    - Edge cases and exceptions
    - Practical applications could be expanded

    **Missing elements to study:**
    - Historical context and development
    - Alternative approaches or methods
    - Common misconceptions to avoid

    **Study Recommendations:**
    - Focus on applying concepts to new problems
    - Create mind maps connecting different ideas
    - Teach the concept to someone else
    - Review past mistakes and corrections

    **Confidence Level:** 70% - Solid foundation with room for deeper understanding.
    """

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