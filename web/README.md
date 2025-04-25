# Debate Stimulator Web Application

This web application provides a browser-based interface for the Debate Stimulator, allowing users to practice British Parliamentary debate with AI opponents.

## Project Structure

The project is divided into two main parts:

- **Backend** (FastAPI): Interfaces with the core Debate Stimulator Python code
- **Frontend** (React): Provides a user-friendly interface for configuring and participating in debates

## Setup & Installation

### Backend Setup

1. Install dependencies:
   ```bash
   cd web/backend
   pip install -r requirements.txt
   ```

2. Run the backend server:
   ```bash
   cd web/backend
   uvicorn main:app --reload
   ```
   The backend will be available at http://localhost:8000

### Frontend Setup

1. Install dependencies:
   ```bash
   cd web/frontend
   npm install
   ```

2. Run the development server:
   ```bash
   cd web/frontend
   npm start
   ```
   The frontend will be available at http://localhost:3000

## Features

- Create new debates with customizable motions
- Configure which debate positions are played by humans vs AI
- Record and transcribe speeches using your microphone
- Generate AI speeches for non-human positions
- View debate history and past performances
- Modern, responsive UI built with Chakra UI

## Deployment

Use the `deploy.sh` script to deploy both the backend and frontend:

```bash
./web/deploy.sh
```

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: React, Chakra UI
- **Audio Processing**: Web Audio API
- **API Communication**: Axios
