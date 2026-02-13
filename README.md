# 🔐 AI-Based Password Strength Checker

A full-stack web application that evaluates password security using Machine Learning, Entropy analysis, and real-world breach database checks.

## 🚀 Features

- **True AI Evaluation**: Uses a Random Forest classifier trained on character n-grams to detect complex patterns.
- **Granular Scoring (0-100)**: Sophisticated scoring mechanism combining AI predictions, Shannon entropy, and heuristic security rules.
- **Data Breach Check**: Integration with the "Have I Been Pwned" API using k-anonymity (secure hashing) to warn if a password has been leaked previously.
- **Dynamic Real-Time Feedback**: Intelligent suggestions that update as you type, only showing what's actually missing.
- **Modern Interactive UI**: 
  - Dynamic strength meter (Red $\rightarrow$ Orange $\rightarrow$ Green).
  - Animated gradient background.
  - Interactive card lifting effects.
  - Secure "Show/Hide" password toggle.
- **Privacy Focused**: Passwords are never stored or logged. Breach checks use anonymized hash prefixes.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Machine Learning**: Scikit-Learn (Random Forest, TF-IDF Vectorization)
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6+)
- **APIs**: Have I Been Pwned (k-anonymity)

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd AI-Based-Password-Strength-Checker
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the AI Model**:
   ```bash
   python model_train.py
   ```

## 🏃 Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser**:
   Navigate to `http://127.0.0.1:5000`

## 🧪 Testing

You can verify the backend logic (Entropy, API, AI) independently by running:
```bash
python test_features.py
```

## 🔒 Security Recommendations

- This app follows the modern security standard of recommending at least **12 characters**.
- It checks for uppercase, lowercase, numbers, and special characters.
- It detects common weak patterns via the AI model.

---
*Created as a demonstration of AI application in Cybersecurity.*
