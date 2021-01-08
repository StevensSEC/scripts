#!usr/bin/python3
from collections import namedtuple
import os
import requests
import re
import sys
import json
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

def do_prompt():
    print("Select a project: \n")
    for project in projects:
        print_project_option(project)

    user_id_selection = -1
    while check_id_selection(user_id_selection) != "OK":
        user_id_selection = input()
        print_selection_error(user_id_selection)

    return int(user_id_selection)

def print_project_option(project):
    print(f"{project.option_id}: {project.name} \n")

def check_id_selection(selection):
    try:
        selection = int(selection)
    except:
        return "Not an int"

    if selection > next_option_id - 1 or selection < 0:
        return "Out of range"

    return "OK"

def print_selection_error(selection):
    if check_id_selection(selection) == "Not an int":
        print(f"{selection} is not a valid option, input an int to select a project")
        return
    user_id_selection = int(selection)
    if check_id_selection(selection) == "Out of range":
        print(f"Selection {selection} was not listed")

selected_project = None
if len(sys.argv) < 2:
    user_id_selection = do_prompt()

    # Get the selected project
    for project in projects:
        if project.option_id == user_id_selection:
            selected_project = project
    assert selected_project != None
else:
    selected_project_name = sys.argv[1]

    for project in projects:
        if project.name.lower() == selected_project_name.lower():
            selected_project = project

    if selected_project == None:
        print(f"Was unable to find a project with the name {selected_project_name}")
        sys.exit()

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

output = {"contributors": users, "referenced_prs": pull_requests}

# Create an output file if the user used the prompt, else output directly to stdout
output_file = open("output.json", "x+") if len(sys.argv) < 2 else sys.stdout
json.dump(output, output_file, indent="\t")
