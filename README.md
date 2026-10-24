# Smart College Study Assistant 🎓

A Fetch.ai **uAgents** chat agent designed to help college students study. It uses the ASI:One API for AI-generated answers and the uAgents chat protocol so it can be tested with Agentverse-compatible chat tools.

## Features

- Explain college subjects in simple language
- Step-by-step maths and engineering help
- Study plans, revision notes, quizzes, and flashcards
- Programming explanations and debugging help
- Chat protocol support for Agentverse-compatible clients

## Project files

- `agent.py` — main uAgent
- `requirements.txt` — Python dependencies
- `.env.example` — environment variable template
- `.gitignore` — prevents secrets and local files from being uploaded

## Requirements

- Python 3.10–3.13 recommended
- An ASI:One API key
- An Agentverse account if you want to inspect/connect the local agent through Agentverse

## Run locally

1. Create a virtual environment and install packages:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your own API key and a unique seed phrase.

   Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

   macOS/Linux:

   ```bash
   cp .env.example .env
   ```

4. Start the agent:

   ```bash
   python agent.py
   ```

5. Check the terminal output for the agent address and Agent Inspector link. Use the inspector/Agentverse workflow to test the agent.

## Publish to GitHub

Create an **empty** repository on GitHub, for example `smart-college-study-assistant`. Do not add a README on GitHub if you already have this one.

From this project folder:

```bash
git init
git add .
git commit -m "Build Smart College Study Assistant agent"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/smart-college-study-assistant.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

**Security:** Never upload `.env`, API keys, or private seed phrases. The `.gitignore` file excludes `.env`; keep it that way. If a secret is accidentally pushed, revoke/rotate it immediately.

## Example prompts

- Explain eigenvalues in simple words with one example.
- Make a 3-day revision plan for my physics exam.
- Explain Python `for` loops and give me a practice question.
- Turn these notes into 5 flashcards: [paste notes].
- Solve this engineering maths problem step by step: [paste problem].

## Notes

- AI answers may be wrong; verify important academic information with your lecturer or course materials.
- The agent does not automatically know your personal timetable, notes, or college portal. Share relevant information in the chat when you want it used.
- This starter project sends each message to the ASI:One API. Check the provider's current terms and pricing before use.
