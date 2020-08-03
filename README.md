# SEC Scripts

These folders contains automation scripts for various tasks.

### Setup

1. Set up a virtual env
```
virtualenv .env -p python3
```

2. Install packages
```
pip install -r requirements.txt
```

### Usage

To run any of the scripts here, from the root folder:

```bash
source .env/bin/activate # only need to do this once.
python3 FOLDERNAME
```

Here is the complete list of scripts:

- `attendance-elibility`: Find out how many events a person has attended based on their name.
- `github-mass-inviter`: Invite all the usernames inputed on stdin to the StevensSEC org, and add them to a given team.
