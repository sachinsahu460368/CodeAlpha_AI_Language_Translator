# Language Translator Backend

FastAPI backend for the AI Language Translator frontend. This project exposes REST APIs only and does not render or modify any frontend files.

## Folder Structure

```text
backend/
|-- app.py
|-- translator.py
|-- language.py
|-- models.py
|-- config.py
|-- requirements.txt
|-- .env
|-- .gitignore
`-- README.md
```

## Installation

Open a terminal in the `backend` folder:

```bash
cd backend
```

## Virtual Environment

Create and activate a Python virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Package Installation

```bash
pip install -r requirements.txt
```

## Running FastAPI

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### GET `/`

Health check.

Response:

```json
{
  "message": "Language Translator API Running"
}
```

### GET `/languages`

Returns supported language names and codes.

Response:

```json
[
  {
    "name": "English",
    "code": "en"
  },
  {
    "name": "Hindi",
    "code": "hi"
  }
]
```

### POST `/translate`

Translates text from source language to target language.

Request:

```json
{
  "text": "Hello",
  "source": "en",
  "target": "hi"
}
```

Response:

```json
{
  "success": true,
  "translated_text": "नमस्ते",
  "source": "English",
  "target": "Hindi"
}
```

### POST `/detect`

Detects the language of text.

Request:

```json
{
  "text": "नमस्ते"
}
```

Response:

```json
{
  "language": "Hindi",
  "code": "hi"
}
```

## CORS

CORS is enabled for:

```text
http://127.0.0.1:3000
http://localhost:3000
```

## Notes

- Translation and detection use `deep-translator`.
- Settings are loaded from `.env` using `pydantic-settings` and `python-dotenv` support.
- Validation is handled with Pydantic models and FastAPI HTTP errors.
- Logs are emitted for API startup, translation requests, successes, and failures.
