# Setup

1. Get a github personal access token with permissions to edit orgs
2. Keep it in a safe place, **DO NOT COMMIT IT.**

# Usage

1. Create a list of usernames or emails that you want to invite to the github org.

2. Note: `TEAM` is optional.
```
cat user-list.txt | GITHUB_USERNAME="YOUR_USERNAME" GITHUB_TOKEN="YOUR GITHUB TOKEN" python3 github-mass-inviter [TEAM]
```

3. Users can accept invites by using the link in their email? (Need confirmation)
