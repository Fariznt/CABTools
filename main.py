# I'm just using this file for testing and stuff. Pls ignore

import requests

# Base URLs for the CAB API
search_url = "https://cab.brown.edu/api/?page=fose&route=search&is_ind_study=N&is_canc=N"
details_url = "https://cab.brown.edu/api/?page=fose&route=details"

# Payload for the search request
search_payload = {
    "other": {"srcdb": "202410"},
    "criteria": [
        {"field": "is_ind_study", "value": "N"},
        {"field": "is_canc", "value": "N"}
    ]
}

# Function to fetch all available courses
def fetch_all_courses():
    response = requests.post(search_url, json=search_payload)
    courses_info = []

    if response.status_code == 200:
        data = response.json()
        # Assuming the relevant course information is in 'results'
        for course in data.get('results', []):
            # Format the course_info according to your required payload structure
            course_info = {
                "group": f"code:{course.get('code')}",  # formatted as "code:COURSE_ID"
                "key": f"crn:{course.get('crn')}",      # formatted as "crn:CRN"
                "srcdb": "202410",                      # semester id
                "matched": f"crn:{course.get('crn')}"   # formatted as "crn:CRN"
            }
            courses_info.append(course_info)
            print(course_info)
    else:
        print(f"Error fetching course info: {response.status_code}")

    return courses_info


# Function to fetch course descriptions
def fetch_course_descriptions(courses):
    for course in courses:
        print("course: " + str(course))
        # Make the request with the current course parameters
        response = requests.post(details_url, json=course)
        print(response)

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            print("data: " + str(data))
            description = data.get('description')
            restriction = str(data.get('registration_restrictions'))

            print(f"Course: {course['group']} - Description: {description}")
            print("registration_restrictions: " + str(restriction))

        else:
            print(f"Error fetching course {course['group']}: {response.status_code}")

def print_postreqs(course_name, courses):
    for course in courses:
        response = requests.post(details_url, json=course)

        if response.status_code == 200:
            data = response.json()
            description = data.get('description')

            #print(f"Considering: {course['group']}")
            if course_name in description:
                print(f"Found: {course['group']}")
        else:
            print(f"Error fetching course {course['group']}: {response.status_code}")

def print_restrictions(course_name, courses):
    for course in courses:
        response = requests.post(details_url, json=course)

        if response.status_code == 200:
            data = response.json()
            restrictions = str(data.get('registration_restrictions'))
            print(f"Considering: {course['group']}")
            if course_name in restrictions:
                print(f"Found: {course['group']}")
                #temp
                print(f"restrictions: {restrictions}")
        else:
            print(f"Error fetching course {course['group']}: {response.status_code}")


# Main execution
all_courses = fetch_all_courses()  # Fetch all available courses
#fetch_course_descriptions(all_courses)  # Fetch and print descriptions for all courses

#print_postreqs("CSCI 0100", all_courses)
print_restrictions("APMA 0360", all_courses)

#to be written
# fetch_all_prerequisites