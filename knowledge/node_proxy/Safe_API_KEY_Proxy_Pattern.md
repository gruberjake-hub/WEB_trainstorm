# Safe API key storage for proxy server

## Symptom
Fear of leaking OpenAI key in GitHub.

## Root Cause
API keys should never be in repo or frontend.

## Fix
proxy_server/.env:
OPENAI_API_KEY=...

In code:
require('dotenv').config()
process.env.OPENAI_API_KEY

## Guardrail
Add to .gitignore:
.env
*.env

Check history:
git log -p | grep -Ei "sk-|api[_-]?key|secret"

## Context
AMLT governed simulation proxy server.

## Tags
security, proxy, api
