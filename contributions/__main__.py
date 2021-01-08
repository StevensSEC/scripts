#!usr/bin/python3
from collections import namedtuple
import os
import requests
import re
from requests.auth import HTTPBasicAuth

# Download metadata for all StevensSEC projects
auth = HTTPBasicAuth(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"])

projects = []
resp = requests.get(f"https://api.github.com/orgs/StevensSEC/projects",
                    headers={'Accept': 'application/vnd.github.inertia-preview.json'},
                    auth=auth)

# Generate list of all projects paired with their project id

Project = namedtuple('Project', 'option_id github_id name')
next_option_id = 0
for project_json in resp.json():
    projects.append(Project(next_option_id, project_json["id"], project_json["name"]))
    next_option_id += 1

# Prompt user to select project from project titles
print("Select a project: \n")

def print_project_option(project):
    print(f"{project.option_id}: {project.name} \n")

for project in projects:
    print_project_option(project)

def check_id_selection(selection):
    try:
        selection = int(selection)
    except:
        return "Not an int"

    if selection  > next_option_id - 1 or selection < 0:
        return "Out of range"

    return "OK"

user_id_selection = -1
while check_id_selection(user_id_selection) != "OK":
    user_id_selection = input()

    if check_id_selection(user_id_selection) == "Not an int":
        print(f"{user_id_selection} is not a valid option, input an int to select a project")
        continue
    user_id_selection = int(user_id_selection)
    if check_id_selection(user_id_selection) == "Out of range":
        print(f"Selection {user_id_selection} was not listed")

# Get the selected project
selected_project = Project(-1, -1, "You shouldnt ever see this.")
for project in projects:
    if project.option_id == user_id_selection:
        selected_project = project

# Download metadata for project columns
resp = requests.get(f"https://api.github.com/projects/{selected_project.github_id}/columns",
                    headers={'Accept': 'application/vnd.github.inertia-preview.json'},
                    auth=auth)

ProjectColumn = namedtuple("ProjectColumn", "github_id name")
columns = []
for columns_json in resp.json():
    columns.append(ProjectColumn(columns_json["id"], columns_json["name"]))

# May be a bit brittle, requires that all contribution boards have "pull request" in their column name
columns = [column for column in columns if "pull request" in column.name.lower()]

# Create a list of all users who added a card in project columns
users = []
notes = []

for column in columns:
    resp = requests.get(f"https://api.github.com/projects/columns/{column.github_id}/cards",
                    headers={'Accept': 'application/vnd.github.inertia-preview.json'},
                    auth=auth)
    for card_json in resp.json():
        users.append(card_json["creator"]["login"])
        notes.append(card_json["note"])

# Filter out duplicates
users = list(set(users))

# Create a list of all referenced pull requests from project column for submitted pull requests

pull_requests = []

# Split all notes into their component lines
notes = [note.split("\n") for note in notes]
# Flatten list
notes = [note for note_list in notes for note in note_list]
# Check all lines
for note in notes:
#   If line is a pull request url
    if (match := re.search(r"https://github.com/(\w|\d)+/(\w|\d)+/(pull|issues)/\d+", note)):
        pull_requests.append(match.group())

pull_requests = list(set(pull_requests))

# Display lists

print("\nUsers who contributed on this board:")
for user in users:
    print(user)

print("\nPull requests and issues referenced on this board:")
for pull_request in pull_requests:
    print(pull_request)
