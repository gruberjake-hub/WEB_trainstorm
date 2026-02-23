# node_modules accidentally staged

## Symptom
git add -A staged thousands of proxy_server/node_modules files.

## Root Cause
.gitignore was in cgen/ instead of repo root and node_modules had already been tracked.

## Fix
cd WEB_trainstorm
mv cgen/.gitignore ./.gitignore
git rm -r --cached AMLT_Governed_Simulation/.../proxy_server/node_modules
git commit -m "Stop tracking node_modules"

## Guardrail
Add to root .gitignore:
**/node_modules/
.env
*.env

## Context
AMLT_Governed_Simulation proxy server setup.

## Tags
git, node, proxy, amltsim
