# Setup

1. Get a github personal access token with permissions to edit orgs
2. Keep it in a safe place, **DO NOT COMMIT IT.**

# Usage

1. Run
```bash
GITHUB_USERNAME=your_username GITHUB_TOKEN=your_token python3 contributions name
```

where `your_username` is your Github username, `your_token` is a Github token with admin:org priveleges, and `name` is the name of the contributions board that you would like to summarize. A successful run will result in a JSON summary being printed.

If you don't know the title of the contributions board that you would like or don't want to supply a name then instead run

```bash
python3 contributions
```

You should see a prompt appear. Input the number that corresponds to the board whose contributions you would like summarized and hit <Enter>. The JSON summary will not be printed directly, and instead will appear in a file called `output.json` in the same directory.
