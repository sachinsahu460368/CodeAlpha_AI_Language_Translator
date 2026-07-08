# 🌍 AI Language Translator

A full-stack AI-powered language translator that detects the language of any input text and translates it into 100+ languages in real time. Built with **FastAPI** on the backend and **vanilla HTML, CSS, and JavaScript** on the frontend.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python 3.11"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange" alt="Frontend"/>
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen" alt="Status"/>
</p>

---

## 📑 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Testing](#-testing)
- [Challenges Solved](#-challenges-solved)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🔎 Overview
This project was built as **Internship Task 1** to demonstrate full-stack development skills — integrating a Python backend with a responsive, interactive frontend. The app allows users to type or paste text, automatically detect its language, and translate it into a language of their choice, with history tracking and a polished dark-mode UI.

---

## ✨ Features
| Feature | Description |
|---|---|
| 🔤 Language Detection | Automatically identifies the language of the entered text |
| 🌐 Multi-language Translation | Translate text into 100+ supported languages |
| 🕘 Translation History | View and revisit previously translated text |
| 🌙 Dark Mode | Toggle between light and dark themes |
| 📋 Copy / Download | Copy translated text or download it as a file |
| 📱 Responsive UI | Works seamlessly across desktop, tablet, and mobile |
| 📘 Swagger API Docs | Interactive API documentation via FastAPI's built-in Swagger UI |
| 🔊 Text-to-Speech | output via Google Cloud TTS |

---

## 🛠 Tech Stack
**Frontend**
- HTML5
- CSS3
- JavaScript (Vanilla)

**Backend**
- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- Deep Translator (translation engine)

---

## 📂 Project Structure
```text
AI-Language-Translator/
├── assets/                # Static assets (icons, images)
├── backend/
│   ├── app.py             # FastAPI application entry point
│   └── requirements.txt   # Python dependencies
├── screenshots/           # App screenshots for documentation
├── index.html             # Frontend entry point
├── style.css              # Styling and dark mode
├── script.js              # Frontend logic and API calls
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/AI-Language-Translator.git
   cd AI-Language-Translator
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the backend server**
   ```bash
   uvicorn app:app --reload
   ```

6. **Access the app**
   - API docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Open `index.html` in your browser to launch the frontend, or serve it via a live server extension.

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Health check — confirms the API is running |
| `GET` | `/languages` | Returns the list of supported languages |
| `POST` | `/detect` | Detects the language of the input text |
| `POST` | `/translate` | Translates input text into the target language |

**Example Request — `/translate`**
```json
{
  "text": "Hello, how are you?",
  "target_lang": "hi"
}
```

**Example Response**
```json
{
  "translated_text": "नमस्ते, आप कैसे हैं?",
  "source_lang": "en",
  "target_lang": "hi"
}
```
---
# 📸 Screenshots

| Home | Translation |
|------|-------------|
| ![](screenshots/home.png) | ![](screenshots/translation.png) |

| Dark Mode | History |
|-----------|---------|
| ![](screenshots/darkmode.png) | ![](screenshots/history.png) |

| Swagger API | Mobile View |
|-------------|-------------|
| ![](screenshots/swagger.png) | ![](screenshots/mobile.png) |
---
## ✅ Testing
- **Functional testing** — Verified core translation and detection logic across multiple language pairs.
- **API testing** — Validated all endpoints via Swagger UI and manual requests.
- **UI testing** — Checked layout consistency, dark mode toggling, and copy/download actions.
- **Responsive testing** — Confirmed usability across desktop, tablet, and mobile screen sizes.

All major test cases passed successfully.

---

## 🧩 Challenges Solved
- Integrating the frontend and backend seamlessly across separate origins
- Handling Unicode text correctly during language detection
- Persisting and displaying translation history
- Implementing robust error handling for invalid/empty input
- Building a fully responsive UI without a frontend framework

---

## 🎥 Demo Video

👉 https://www.loom.com/share/54515340e4e34b0a804f2a0e2b5779ae
---

## 🚀 Future Improvements
- 🎙️ Speech-to-Text input support
- 🖼️ OCR-based translation (translate text from images)
- ☁️ Cloud deployment (Render / Vercel / Railway)

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome. Feel free to open a pull request or file an issue.

---



# 👨‍💻 Author

## Sachin Sahu

Hi! I'm **Sachin Sahu**, a passionate Computer Science student with a strong interest in **Artificial Intelligence, Machine Learning, Generative AI, Agentic AI, and Full-Stack Development**. I enjoy building real-world applications that solve practical problems while continuously learning modern technologies.

This project was developed as **Task 1 of my AI Internship**, where I designed and implemented a complete full-stack language translation application. Throughout this project, I gained hands-on experience in backend API development, frontend integration, debugging, testing, and project documentation.

---
# 🙏 Acknowledgements

I would like to thank my internship mentors and the open-source community for providing excellent tools and resources that made this project possible.

Special thanks to the developers of:

- FastAPI
- Deep Translator
- Uvicorn
- Pydantic
- Python
- HTML, CSS & JavaScript
---
### 🚀 Areas of Interest
---

- Artificial Intelligence (AI)
- Generative AI & Large Language Models (LLMs)
- Agentic AI Systems
- Machine Learning
- Natural Language Processing (NLP)
- Full-Stack Web Development
- Python Development
- FastAPI
- JavaScript
---
### 🛠 Skills
---
- Python
- FastAPI
- HTML5
- CSS3
- JavaScript
- REST APIs
- Git & GitHub
- VS Code
- C/C++
---
# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.

Your support motivates me to build more AI and Full-Stack projects.
---

### 📬 Connect with Me
---
- GitHub: https://github.com/sachinsahu460368
- LinkedIn: https://www.linkedin.com/in/sachin-sahu-ba9568380
- Email: sachinsahu300905@gmail.com

> *"I believe that continuous learning and building real-world projects are the best ways to grow as a software developer."*
