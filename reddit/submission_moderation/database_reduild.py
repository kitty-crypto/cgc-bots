import os
import sys
# Functions related to database rebuild.
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.split(os.path.dirname(current))[0]
sys.path.append(f"{parent_directory}/common")
from database import database

db = database("database.db")

# Repopulates the database of questions
def update_question_database(submission):
  if "Question" in submission.link_flair_text:
    db[submission.id] = submission.title

# Deletes all elements from the database
def delete_question_database():
  keys_to_delete = list(db.keys()).remove("whitelist")
  
  for i, val in enumerate(keys_to_delete):
    del db[val]

