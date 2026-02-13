from flask import Flask, render_template, request, jsonify
import joblib
import os
import re
import math
import hashlib
import requests

app = Flask(__name__)

# Load Model and Vectorizer
MODEL_PATH = 'password_model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    print("Model files not found. Please run model_train.py first.")
    model = None
    vectorizer = None

def calculate_entropy(password):
    """Calculates the Shannon entropy of a password."""
    if not password:
        return 0
    
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'\d', password): charset_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): charset_size += 32
    
    if charset_size == 0:
        return 0
        
    return len(password) * math.log2(charset_size)

def check_pwned_api(password):
    """Checks if password exists in Have I Been Pwned database (k-anonymity)."""
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1password[:5], sha1password[5:]
    
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=2)
        if response.status_code != 200:
            return 0
            
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
        return 0
    except:
        return -1 # Error checking

def get_dynamic_feedback(password, score, breach_count):
    """Generates dynamic feedback based on missing requirements and status."""
    feedback = []
    
    if breach_count > 0:
        feedback.append(f"⚠️ Security Alert: This password has appeared in {breach_count} data breaches! Change it immediately.")
    
    if len(password) < 12:
        feedback.append("Increase password length to at least 12 characters.")
        
    if not re.search(r"[A-Z]", password):
        feedback.append("Add uppercase letters.")
        
    if not re.search(r"[a-z]", password):
        feedback.append("Add lowercase letters.")
        
    if not re.search(r"\d", password):
        feedback.append("Add numbers.")
        
    if not re.search(r"[!@#$%^&*]", password):
        feedback.append("Add special characters (e.g. !@#$).")
    
    # AI/Entropy based generic advice if technically valid but still weak
    if score < 50 and not feedback:
        feedback.append("Avoid common words or patterns. Try a passphrase.")
        
    return feedback

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if not model or not vectorizer:
        return jsonify({'error': 'Model not loaded'}), 500
        
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'score': 0, 'feedback': [], 'breached': 0})

    # 1. AI Prediction (Probability)
    features = vectorizer.transform([password])
    # Class order usually [Medium, Strong, Weak] or similar, check classes_
    # We'll map classes to a coarse score, then refine with entropy
    
    prediction_cls = model.predict(features)[0]
    # Get probability of 'Strong' class if available, else standard mapping
    # For simplicity, we stick to our mapping + entropy hybrid since the model was trained on simple classes
    
    # 2. Entropy Calculation
    entropy = calculate_entropy(password)
    
    # 3. Breach Check
    breach_count = check_pwned_api(password)
    
    # 4. Final Score Calculation (0-100)
    # Base score from logic
    base_score = 0
    if len(password) >= 8: base_score += 20
    if len(password) >= 12: base_score += 20
    if re.search(r"[A-Z]", password): base_score += 10
    if re.search(r"[a-z]", password): base_score += 10
    if re.search(r"\d", password): base_score += 10
    if re.search(r"[!@#$%^&*]", password): base_score += 10
    
    # AI adjustment (If AI says Strong/Medium, boost/penalize)
    if prediction_cls == 'Strong': base_score += 20
    elif prediction_cls == 'Weak': base_score -= 20
    
    # Cap score
    final_score = min(100, max(0, base_score))
    
    # Hard Penalties
    if breach_count > 0:
        final_score = 0 # Breached passwords are effectively 0 strength
    
    # 5. Feedback
    feedback = get_dynamic_feedback(password, final_score, breach_count)
    
    return jsonify({
        'score': final_score,
        'entropy': round(entropy, 2),
        'breach_count': breach_count,
        'feedback': feedback,
        'ai_prediction': prediction_cls
    })

if __name__ == '__main__':
    app.run(debug=True)
