# pr_writer

A CLI tool that automatically generates professional GitHub pull request titles and descriptions from your `git diff`, powered by Claude AI.

## What it does

Run it inside any git repo and it will:
1. Detect your current code changes (`git diff main`)
2. Send the diff to Claude
3. Print a ready-to-use PR title and description in your terminal

## Requirements

- Python 3.10+
- A git repository with changes
- An [Anthropic API key](https://console.anthropic.com)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# 1. Go to your project
cd your-project

# 2. Stage your changes
git add .

# 3. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."   # Mac/Linux
$env:ANTHROPIC_API_KEY = "sk-ant-..."   # Windows PowerShell

# 4. Run the tool
python path/to/pr_writer.py
```

## Example output

```
Generating PR title and description...

**Title:** Add user authentication with JWT tokens

**Description:**
## Summary
- Adds login and logout endpoints with JWT-based session management
- Protects existing routes with an auth middleware

## Key Changes
- `auth.py` — new module handling token generation and validation
- `routes.py` — login/logout endpoints added
- `middleware.py` — `require_auth` decorator applied to protected routes

## Notes
- Tokens expire after 24 hours; refresh logic is not yet implemented
```

## How it works

The tool uses the [`claude-agent-sdk`](https://pypi.org/project/claude-agent-sdk/) to send your diff to Claude (`claude-sonnet-4-6`) with a system prompt instructing it to act as a senior software engineer writing PR documentation.
"# test" 
