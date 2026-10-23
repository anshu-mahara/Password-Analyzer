# 🔐 PasswordGuard — Password Strength Analyzer

PasswordGuard is a Python-based password analysis web application built with Streamlit. It evaluates password strength, identifies common weaknesses, and provides actionable recommendations to help users create stronger passwords.

## ✨ Features

- **Strength Analysis:** Estimates password strength using the `zxcvbn` library.
- **Weakness Detection:** Identifies common passwords, predictable sequences, repeated characters, and recognizable years.
- **Character Analysis:** Checks password length and the use of lowercase letters, uppercase letters, digits, symbols, and spaces.
- **Personalized Recommendations:** Provides suggestions based on detected weaknesses.
- **Interactive Dashboard:** Displays analysis results through a clean interface with a soft pastel theme.
- **Automated Tests:** Includes tests for common inputs and edge cases.

## 🛠️ Technologies Used

- Python
- Streamlit
- zxcvbn
- Pytest

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Navigate to the project folder

```bash
cd YOUR_PROJECT_FOLDER
```

Replace `YOUR_PROJECT_FOLDER` with the name of your project directory.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at `http://localhost:8501`.

## 🧪 Run Tests

Install pytest if needed:

```bash
pip install pytest
```

Then run:

```bash
python -m pytest -v
```

## 📁 Project Structure

```text
PasswordGuard/
├── app.py
├── analyzer.py
├── requirements.txt
├── README.md
└── tests/
    └── test_analyzer.py
```

## 🔒 Privacy and Security

- Use fictional sample passwords when testing the application.
- Do not enter passwords that you currently use for real accounts.
- Password strength estimates are informative and are not a guarantee of security.
- This project is intended for password security awareness and educational purposes.

## 🎯 Project Goal

The goal of PasswordGuard is to make password security easier to understand by combining password-strength estimation, weakness detection, and practical recommendations in one interactive application.

## 👨‍💻 Author

Created as a Python and cybersecurity project to explore password analysis, secure coding practices, automated testing, and web application development.
