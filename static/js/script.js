document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('passwordInput');
    const togglePassword = document.getElementById('togglePassword');
    const strengthBar = document.getElementById('strengthBar');
    const strengthText = document.getElementById('strengthText');
    const feedbackArea = document.getElementById('feedbackArea');
    const suggestionsList = document.getElementById('suggestionsList');

    let debounceTimer;

    // Toggle Password Visibility
    togglePassword.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        togglePassword.textContent = type === 'text' ? '🙈' : '👁️';
    });

    // Real-time Analysis
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;

        // Visual feedback for empty input
        if (!password) {
            resetUI();
            return;
        }

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            analyzePassword(password);
        }, 500); // 500ms debounce (API rate limits / performance)
    });

    async function analyzePassword(password) {
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ password })
            });

            const data = await response.json();
            updateUI(data);

        } catch (error) {
            console.error('Error analyzing password:', error);
            strengthText.textContent = 'Error connecting to server';
        }
    }

    function updateUI(data) {
        const score = data.score; // 0 to 100
        const feedback = data.feedback;
        const breachCount = data.breach_count;
        const entropy = data.entropy;

        // Update Progress Bar Width
        strengthBar.style.width = `${score}%`;

        // Update Color & Text based on Score
        // Remove old classes
        strengthBar.className = 'strength-bar';
        strengthText.className = 'strength-text';

        let strengthLabel = '';
        let colorClass = '';

        if (score < 40) {
            strengthLabel = 'Weak';
            colorClass = 'weak';
        } else if (score < 80) {
            strengthLabel = 'Medium';
            colorClass = 'medium';
        } else {
            strengthLabel = 'Strong';
            colorClass = 'strong';
        }

        // Critical Override for Breached Passwords
        if (breachCount > 0) {
            strengthLabel = '⚠️ Breached!';
            colorClass = 'weak';
            strengthBar.style.backgroundColor = '#ff0000'; // Hard red
        } else {
            strengthBar.classList.add(colorClass);
            strengthBar.style.backgroundColor = ''; // Reset inline style
        }

        strengthText.textContent = `${strengthLabel} (Score: ${score}/100)`;
        strengthText.classList.add(colorClass); // Color the text too

        if (breachCount > 0) {
            strengthText.style.color = '#ff0000';
        } else {
            strengthText.style.color = ''; // Reset
        }

        // Update Suggestions
        suggestionsList.innerHTML = '';
        if (feedback && feedback.length > 0) {
            feedbackArea.classList.remove('hidden');
            feedbackArea.classList.add('visible');

            feedback.forEach(msg => {
                const li = document.createElement('li');
                li.textContent = msg;
                suggestionsList.appendChild(li);
            });
        } else {
            feedbackArea.classList.remove('visible');
            feedbackArea.classList.add('hidden');
        }
    }

    function resetUI() {
        strengthBar.style.width = '0%';
        strengthBar.className = 'strength-bar';
        strengthText.textContent = 'Enter a password to check';
        strengthText.style.color = 'var(--text-primary)';
        strengthText.className = 'strength-text';

        feedbackArea.classList.remove('visible');
        feedbackArea.classList.add('hidden');
        suggestionsList.innerHTML = '';
    }
});
