import joblib
import os
import re

# Simulate the backend logic for testing
MODEL_PATH = 'password_model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

print("Loading model...")
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model loaded successfully.")
else:
    print("Error: Model files not found.")
    exit(1)

def get_password_feedback(password, strength):
    feedback = []
    if len(password) < 8:
        feedback.append("Increase password length to at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        feedback.append("Add uppercase letters.")
    if not re.search(r"[a-z]", password):
        feedback.append("Add lowercase letters.")
    if not re.search(r"\d", password):
        feedback.append("Add numbers.")
    if not re.search(r"[!@#$%^&*]", password):
        feedback.append("Add special characters.")
    if strength == 'Weak' and not feedback:
        feedback.append("Avoid common patterns or words.")
    return feedback

def analyze(password):
    if not password:
        return {'strength': 'Empty', 'feedback': []}
    features = vectorizer.transform([password])
    strength = model.predict(features)[0]
    feedback = get_password_feedback(password, strength)
    return {'strength': strength, 'feedback': feedback}

# Test Cases
passwords = [
    "123456",            # Weak
    "password",          # Weak
    "monKey",            # Weak/Medium?
    "Secret123",         # Medium/Strong
    "MySup3rS3cr3t!Pw"   # Strong
]

print("\n--- Testing Password Analysis ---")
for p in passwords:
    result = analyze(p)
    print(f"Password: '{p}' -> Strength: {result['strength']}")
    if result['feedback']:
        print(f"Feedback: {result['feedback']}")
    print("-" * 30)
