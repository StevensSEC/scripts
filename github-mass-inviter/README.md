# Setup

1. Get a github personal access token with permissions to edit orgs
2. Keep it in a safe place, **DO NOT COMMIT IT.**

# Usage

1. Create a list of usernames or emails that you want to invite to the github org.

2. Note: `TEAM` is optional.
```bash
cat user-list.txt | GITHUB_USERNAME="YOUR_USERNAME" GITHUB_TOKEN="YOUR GITHUB TOKEN" python3 github-mass-inviter [TEAM]
```

3. Users can accept invites by using the link in their email? (Need confirmation)

### Tips

To make this script easier to use, you can set `GITHUB_USERNAME` and `GITHUB_TOKEN` in `.env/bin/activate` and export them.

At the bottom of `.env/bin/activate`:
```bash
export GITHUB_USERNAME="..."
export GITHUB_TOKEN="..."
```
Make sure to unset these variables when you deactivate. At the bottom of the `deactivate` function:
```bash
unset GITHUB_USERNAME
unset GITHUB_TOKEN
```
