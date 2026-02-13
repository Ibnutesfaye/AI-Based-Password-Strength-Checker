import pandas as pd
import numpy as np
import random
import string
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def generate_password(strength):
    """Generate a password of a given strength."""
    if strength == 'Weak':
        # Short, simple, common patterns
        length = random.randint(4, 7)
        chars = string.ascii_lowercase
        if random.random() > 0.5:
             # Common weak passwords base
            base = random.choice(['123456', 'password', 'qwerty', 'welcome', 'love', 'admin'])
            return base[:random.randint(4, len(base))]
        return ''.join(random.choices(chars, k=length))
    
    elif strength == 'Medium':
        # Medium length, mixed case or some numbers
        length = random.randint(8, 11)
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
    
    elif strength == 'Strong':
        # Long, mixed case, numbers, special chars
        length = random.randint(12, 16)
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))

def create_dataset(n_samples=5000):
    """Create a synthetic dataset."""
    data = []
    labels = []
    
    for _ in range(n_samples):
        strength = random.choice(['Weak', 'Medium', 'Strong'])
        password = generate_password(strength)
        data.append(password)
        labels.append(strength)
        
    return pd.DataFrame({'password': data, 'strength': labels})

def extract_features(passwords):
    """
    Extract features manually if needed, but for this simple model 
    we will rely on Character Grams via TfidfVectorizer.
    """
    return passwords

# 1. Generate Data
print("Generating synthetic dataset...")
df = create_dataset(5000)
print(f"Dataset created with {len(df)} samples.")

# 2. Feature Extraction (Character Level TF-IDF)
# Analyzer='char' treats the input as a sequence of characters.
# ngram_range=(1, 4) captures patterns like 'abc', '123'
print("Vectorizing passwords...")
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 4))
X = vectorizer.fit_transform(df['password'])
y = df['strength']

# 3. Train Model
print("Training Random Forest Classifier...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

print(f"Model Accuracy: {clf.score(X_test, y_test):.2f}")

# 4. Save Model and Vectorizer
print("Saving model and vectorizer...")
joblib.dump(clf, 'password_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("Done!")
