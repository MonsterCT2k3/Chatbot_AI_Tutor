# Fullstack AI Tutor (Base Structure)

Here is the initial base structure for your new fullstack project. You can copy this folder to any other location on your computer when you are ready.

## Directory Structure
- `/be` (Backend): Contains all the RAG logic, Chroma Database, API keys (`.env`), and chunking scripts.
- `/fe` (Frontend): Empty folder prepared for your React/Vite application.

## Next Steps

1. **For Backend (BE):**
   - Navigate to the `be/` folder.
   - We will need to create a `main.py` using **FastAPI** to wrap the `4_agent.py` logic into a REST API (e.g., a `POST /api/chat` endpoint).

2. **For Frontend (FE):**
   - You will need to have Node.js installed on the computer where you run this.
   - Navigate to the `fe/` folder.
   - Run `npx create-vite@latest . --template react` (or vue/nextjs) to initialize the frontend code.
   - Build a UI that calls your FastAPI backend.
