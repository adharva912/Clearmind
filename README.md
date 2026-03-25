# ClearMind - Learning Assistant

## Overview
ClearMind is an AI-powered learning platform that helps students master topics through explanation, practice, and reflection. Features user accounts for personalized learning experiences.

## Features
- **User Accounts**: Secure registration and login system
- **AI Topic Explanation**: Get clear, personalized explanations for any topic
- **Self-Explanation Evaluation**: Write your own explanation and get AI feedback
- **Real-World Problem Generation**: Apply concepts to practical scenarios
- **Revision Practice**: Test your knowledge retention
- **Reflection Analysis**: Analyze your thinking process and identify biases
- **Progress Tracking**: Save all your learning activities
- **Mastery Scoring**: Get quantitative feedback on your understanding

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set your Gemini API key: `export GEMINI_API_KEY=your_api_key_here` (or set environment variable)
3. Run: `python app.py`
4. Open http://127.0.0.1:5000
5. Register a new account or login

## Current Status
- ✅ User authentication system (file-based storage)
- ✅ All UI components and pages
- ✅ Real AI responses (Gemini API enabled with Python 3.14.3 compatibility)
- ✅ Data persistence for user activities

## Data Storage
The app uses JSON file-based storage:
- `users.json` - User accounts and authentication
- `user_data/` - Individual user learning data

## API Endpoints
- `POST /explain` - Generate topic explanations
- `POST /evaluate_explanation` - Evaluate student explanations
- `POST /generate_problem` - Create real-world problems
- `POST /revision_check` - Check revision quality
- `POST /analyze_reflection` - Analyze learning reflections
- `POST /calculate_mastery` - Calculate mastery scores

## User Features
- **Secure Authentication**: Password hashing and session management
- **Personal Dashboard**: Access all your learning activities
- **Progress History**: View your past explanations, reflections, and problems
- **Data Persistence**: All your work is saved to your account

## Next Steps
1. **Database Migration**: Consider moving to SQLite/PostgreSQL for production
2. **User Dashboard**: Add pages to view learning history
4. **Progress Analytics**: Visual charts and insights
5. **Export Features**: Allow users to export their data

## Development
The application is currently running with mock AI responses. To enable real AI features, resolve the Google Generative AI compatibility issue with Python 3.14.3.