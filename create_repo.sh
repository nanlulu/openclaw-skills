#!/bin/bash

# Load GitHub token from .env
GITHUB_TOKEN=$(grep '^GITHUB_TOKEN=' .env | cut -d'=' -f2)
REPO_NAME="openclaw-skills"
REPO_DESCRIPTION="OpenClaw skills collection - A curated set of skills for OpenClaw AI assistant"

echo "🚀 Creating new GitHub repository: $REPO_NAME"

# Create repository using GitHub API
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"$REPO_DESCRIPTION\",
    \"private\": false,
    \"has_issues\": true,
    \"has_projects\": false,
    \"has_wiki\": false,
    \"auto_init\": false
  }" 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'html_url' in data:
    print('✅ Repository created successfully!')
    print('📦 Repository URL:', data['html_url'])
    print('📋 SSH URL:', data['ssh_url'])
    print('🔗 Clone URL:', data['clone_url'])
else:
    if 'message' in data:
        print('❌ Error:', data['message'])
    else:
        print('❌ Unknown error occurred')
"