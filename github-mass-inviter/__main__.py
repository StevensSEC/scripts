#!/usr/bin/env python3
import os
import sys
import requests
from requests.auth import HTTPBasicAuth
import json

auth=HTTPBasicAuth(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"])

users = sys.stdin.readlines()
userids = {}
emails = []

print("Getting user ids...")

for user in users:
	user = user.strip()
	if "@" in user:
		emails.append(user)
	else:
		resp = requests.get(f"https://api.github.com/users/{user}")
		if resp.status_code == 200:
			userids[resp.json()["id"]] = user
		else:
			print("Failed to grab user ID:", resp.json())
			sys.exit(1)


team_ids = []
if len(sys.argv) > 1:
	for team in sys.argv[1:]:
		print(f"Grabbing team id for {team}...")
		resp = requests.get(f"https://api.github.com/orgs/StevensSEC/teams/{team}", auth=auth)
		if resp.status_code == 200:
			team_ids.append(resp.json()["id"])
		else:
			print("Failed to grab team ID:", resp.json())
			sys.exit(1)

print(f"Adding {len(userids)} users by userid and {len(emails)} users by email to {team_ids}")

def add_team_memberships(username, teams):
	for team in teams:
		resp = requests.put(f"https://api.github.com/orgs/StevensSEC/teams/{team}/memberships/{username}", auth=auth)
		print(f"put user {username} in {team}: {resp.status_code}")
		if resp.status_code != 200:
			print(f"error: {resp.json()}")

for email in emails:
	resp = requests.post("https://api.github.com/orgs/StevensSEC/invitations", data=json.dumps({
		"email": email,
		"team_ids": team_ids
	}), auth=auth)
	print(f"invite user {email}: {resp.status_code}")
	if resp.status_code != 201:
		print(f"error: {resp.json()}")
already_in_org = []
for userid in userids:
	resp = requests.post("https://api.github.com/orgs/StevensSEC/invitations", data=json.dumps({
		"invitee_id": userid,
		"team_ids": team_ids
	}), auth=auth)
	print(f"invite user {userid}: {resp.status_code}")
	if resp.status_code != 201:
		if resp.status_code == 422 and resp.json()["errors"][0]["resource"] == "OrganizationInvitation":
			print(f"{userid} is already in org")
			already_in_org += [userid]
		else:
			print(f"error: {resp.json()}")

for userid in already_in_org:
	user = userids[userid]
	add_team_memberships(user, sys.argv[1:])
