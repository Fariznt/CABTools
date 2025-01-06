import sqlite3

# This script prints a list of courses that have a description or course restrictions
# that mention the class defined by variable PREREQ_CODE
# Make sure create_db.py has been run for this semester before (see README)

# class code of class for which you want to check for post-requisite and other relations
# Must be formatted "XXXX 0000"
PREREQ_CODE = "APMA 0360"

# semester id, CHANGE for every semester
SEM_ID = 202420 # the semester being looked through

# Create/connect to database of courses
connection = sqlite3.connect(str(SEM_ID) + "_cab_base")
# Create cursor for interaction w/ database
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(my_table)")
print(cursor.fetchall())

cursor.execute("SELECT code, description, restrictions FROM my_table") # select description column from database
courses = cursor.fetchall() # fetch all descriptions (as tuples of length one)


for course in courses:
    code = course[0]
    description = course[1]
    restriction_string = course[2]
    if PREREQ_CODE in description or PREREQ_CODE in restriction_string:
        print(code)