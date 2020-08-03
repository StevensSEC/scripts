#!/usr/bin/env python3
import os
import sys
import requests
from requests.auth import HTTPBasicAuth
import json

auth=HTTPBasicAuth(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"])

users = sys.stdin.readlines()
userids = []
emails = []

print("Getting user ids...")

for user in users:
	if "@" in user:
		emails.append(user)
	else:
		resp = requests.get(f"https://api.github.com/users/{user}")
		if resp.status_code == 200:
			userids.append(resp.json()["id"])
		else:
			print("Failed to grab user ID:", resp.json())
			sys.exit(1)


team_ids = []
if len(sys.argv) > 1:
	print("Grabbing team id...")
	resp = requests.get(f"https://api.github.com/orgs/StevensSEC/teams/{sys.argv[1]}", auth=auth)
	if resp.status_code == 200:
		team_ids.append(resp.json()["id"])
	else:
		print("Failed to grab team ID:", resp.json())
		sys.exit(1)

print(f"Adding {len(userids)} users by userid and {len(emails)} users by email.")

for email in emails:
	resp = requests.post("https://api.github.com/orgs/StevensSEC/invitations", data=json.dumps({
		"email": email,
		"team_ids": team_ids
	}), auth=auth)
	print(f"invite user {email}: {resp.status_code}")
	if resp.status_code != 201:
		print(f"error: {resp.json()}")
for userid in userids:
	resp = requests.post("https://api.github.com/orgs/StevensSEC/invitations", data=json.dumps({
		"invitee_id": userid,
		"team_ids": team_ids
	}), auth=auth)
	print(f"invite user {userid}: {resp.status_code}")
	if resp.status_code != 201:
		print(f"error: {resp.json()}")
