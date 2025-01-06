import sqlite3
import requests

# id for semester for which database is created, CHANGE for every semester
SEM_ID = 202410

# Create/connect to database of courses
connection = sqlite3.connect(str(SEM_ID) + "_cab_base")
# Create cursor for interaction w/ database
cursor = connection.cursor()

# Make table for storing string course description data
cursor.execute("DROP TABLE IF EXISTS my_table") # temp. need to delete old tables while i change the code and test
cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        description TEXT,
        restrictions TEXT
        )
    """)

# Base URLs for the CAB API
search_url = "https://cab.brown.edu/api/?page=fose&route=search&is_ind_study=N&is_canc=N"
details_url = "https://cab.brown.edu/api/?page=fose&route=details"

# Payload for the search request
search_payload = {
    "other": {"srcdb": SEM_ID},
    "criteria": [
        {"field": "is_ind_study", "value": "N"},
        {"field": "is_canc", "value": "N"}
    ]
}

response = requests.post(search_url, json=search_payload)

if response.status_code == 200:
    courses_data = response.json()
    # Assuming the relevant course information is in 'results'...
    # Traverse each course within post request data and append its description to course_description_list
    for course in courses_data.get('results', []):
        # Format the course_info according to your required payload structure
        # Create payload for details post request using course
        details_payload = {
            "group": f"code:{course.get('code')}",  # formatted as "code:COURSE_ID"
            "key": f"crn:{course.get('crn')}",  # formatted as "crn:CRN"
            "srcdb": SEM_ID,  # semester id
            "matched": f"crn:{course.get('crn')}"  # formatted as "crn:CRN"
        }
        # Make post request for details of this course
        response = requests.post(details_url, json=details_payload)
        if response.status_code == 200: # if response for details was successful
            this_course_data = response.json()
            # save course description in variable
            description = this_course_data.get('description')
            # save registration restrictions as string. If empty, save as "" so restrictions is never None
            restrictions = str(this_course_data.get('registration_restrictions') or "")
            code = course.get('code') # get class code (ex. MATH 0100)

            cursor.execute(
                "INSERT OR IGNORE INTO my_table (code, description, restrictions) VALUES (?, ?, ?)",
                (code, description, restrictions))
        else:
            print(f"Error fetching a course {course['group']}: {response.status_code}")

        print("Added course " + course.get('code') + " to database, if not already added.")
else:
    print(f"Error fetching courses: {response.status_code}")

connection.commit() # save changes
connection.close() # close connection

