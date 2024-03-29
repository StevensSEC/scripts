from os import listdir
import pandas as pd

# Load DuckLink's attendance .csv files
directory = 'attendance-eligibility/' + \
    input('Enter the name of the directory containing attendance csv files:\n') + '/'
files = [f for f in listdir(directory)]
cols = ['First Name', 'Last Name', 'Email']

members = {}

for file in files:

    # Create a DataFrame object for each new CSV file
    df = pd.read_csv(directory + file, names=cols)

    # Get event name
    event_name = df.at[1, 'First Name']

    # Trim everything up to the first and last names
    starting_names_line_num = 6
    df = df[starting_names_line_num:]

    for i in range(starting_names_line_num, len(df) + starting_names_line_num):

        # Parse out some key information
        first_name = df.at[i, 'First Name']
        last_name = df.at[i, 'Last Name']
        full_name = first_name + " " + last_name
        email = df.at[i, 'Email']

        # If the person exists, update their info, otherwise start a new entry
        if full_name in members:
            members[full_name]['attended_events'].append(event_name)
            members[full_name]['events_attended'] += 1
        else:
            members[full_name] = {
                'email': email,
                'attended_events': [event_name],
                'events_attended': 1
            }

voting_members = {}

for member, obj in members.items():
    if obj['events_attended'] >= 3:
        voting_members[member] = obj['events_attended']

print(voting_members)
