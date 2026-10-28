# RADIX Resume Parsing

A resume parsing application that extracts structured candidate information from PDF and DOCX resumes, including contact details, technical skills, education, projects, and experience.

## Features

- Upload resumes in PDF and DOCX formats.
- Extract candidate information into structured data.
- Manual extraction mode without hosted AI processing.
- Optional AI-powered extraction using the Groq API, with user consent.
- Validate extracted skills and flag information that needs review.
- FastAPI backend and React frontend.
- File size limit: 5 MB.

## Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Pydantic
- Uvicorn
- Groq API (optional AI extraction)
- PyPDF and python-docx for document reading

## Project Structure

```text
radix-resume-parsing/
├── backend/
│   └── app/
│       ├── tests/
│       ├── main.py
│       ├── extractor.py
│       ├── manual_extractor.py
│       ├── models.py
│       └── reader.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── samples/
├── .gitignore
└── README.md
```

## Requirements

Install the following before running the project:

- Python 3.12
- Node.js and npm
- Git

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/nihar2610/resume-parcing.git
cd resume-parcing
```

### 2. Set up the backend

Create and activate a virtual environment from the project root.

**Windows PowerShell:**

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
python -m pip install fastapi uvicorn pydantic python-multipart python-dotenv pypdf python-docx groq httpx pytest
```

### 3. Configure the environment

Create a `.env` file in the project root and add your own Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit or share your actual API key.

### 4. Start the backend

From the project root, run:

```powershell
python -m uvicorn backend.app.main:app --reload
```

Backend API: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 5. Set up the frontend

Open a second terminal and run:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually:

http://localhost:5173

Keep both the backend and frontend terminals running while using the application.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/team/v1/health` | Check backend health |
| POST | `/api/team/v1/resumes/extract` | Extract information from a resume |

The extraction endpoint accepts PDF and DOCX files up to 5 MB.

## Running Tests

From the project root, activate the backend virtual environment and run:

```powershell
python -m pytest backend/app/tests -q
```

## Security and Privacy

- Keep API keys in the local `.env` file.
- Never commit `.env`, virtual environments, or `node_modules`.
- AI-powered extraction sends resume text to the Groq API only when the user opts in.
- Use test resumes or obtain permission before processing real candidates' personal information.

## Project Status

RADIX Resume Parsing is under development. Extracted information should be reviewed for accuracy before being used in recruitment decisions.
