import os
import re
import json
import shutil


class DatabaseError(Exception):
  pass

class database:
  # Constructor method for the class, takes a string argument 'db_location' and sets two instance variables
  def __init__(self, db_location: str) -> None:
    self.__db_location = db_location  # A private instance variable to hold the database location
    self.__database = {}  # A private instance variable to hold the contents of the database as a dictionary
    try:
      self.__update_db()  # Try to update the contents of the database using the private method '__update_db()'
    except FileNotFoundError:
      self.__save_db()  # If the database file is not found, save the current contents of the database to a new file

  # A private method that reads the contents of the database file and updates the instance variable '__database' with its contents
  def __update_db(self):
    # Create a backup of the database file
    backup_location = self.__db_location + '.bak'
    if os.path.exists(backup_location):
      os.remove(backup_location)
    shutil.copy(self.__db_location, backup_location)  

    with open(self.__db_location, 'r') as dbl:
      try:
        self.__database = json.loads(self.__try_fix_db_syntax(dbl))
      except:
        raise DatabaseError("Database error: The database file is corrupted")
    # Update the database contents from the file
    with open(self.__db_location, 'r') as dbl:
      self.__database = json.loads(dbl.read())



  # Attempt to fix the syntax of the dayabase file by adding any missing } or {, if possible
  def __try_fix_db_syntax(self, dbl):
    contents = dbl.read()
    num_open = contents.count('{')
    num_close = contents.count('}')
    if num_open > num_close:
      contents += '}' * (num_open - num_close)
    elif num_close > num_open:
      contents = contents[:contents.rfind('}')] + ('{' * (num_close - num_open)) + contents[contents.rfind('}') + 1:]
      dbl.seek(0)
    try:
      json.loads(contents)
    except ValueError:
      # remove non-json characters and try again
      contents = re.sub(r'\s*\w+\s*:', lambda m: '"' + m.group().strip() + '":', contents)
      contents = re.sub(r"'", '"', contents)
    return json.dumps(json.loads(contents))

  # A private method that saves the contents of the instance variable '__database' to the database file
  def __save_db(self):
    with open(self.__db_location, 'w+') as dbl:
      json.dump(self.__database, dbl)

  # A magic method that allows the class instance to be updated with new key-value pairs
  def __setitem__(self, *args):
    # If odd number of arguments, assign empty value to last key
    if len(args) % 2 == 1:
      empty_key = args[-1]
      if empty_key in self.__database:
        self.__database[empty_key] = None
      else:
        self.__database.update({empty_key: None})
      args = args[:-1]
    # Assign values to corresponding keys
    for k, v in zip(args[0::2], args[1::2]):
      if isinstance(v, database):
        value = {'path': v.get_path(), 'class': 'database'}
      else:
        value = v
      if k in self.__database:
        self.__database[k] = value
      else:
        self.__database.update({k: value})
    # Save changes to database file
    self.__save_db()
    # Update in-memory database instance
    self.__update_db()

  # A magic method that allows the class instance to have key-value pairs removed
  def __delitem__(self, k):
    del self.__database[k]
    self.__save_db()

  # A magic method that allows the class instance to be indexed by key, returning the corresponding value
  def __getitem__(self, k):
    self.__update_db()
    value = self.__database.get(k)
    if isinstance(value, dict) and value.get('class') == 'database':
      return database(value.get('path'))
    return value

  # Customises how instances of the class are represented as strings.
  def __str__(self):
    self.__update_db()
    return f"<database object at {id(self)}>\n  contents: {str(self.__database)}"

  # A method that returns an empty dictionary, effectively clearing the contents of the database
  def clear(self):
    return self.__do_to_db('clear')

  # A method that returns a shallow copy of the instance variable '__database'
  def copy(self):
    return self.__do_to_db('copy')

  # A method that returns the value associated with the specified key, or None if the key is not found
  def get(self, k):
    return self.__do_to_db('get', f"'{k}'")

  '''
  # A method that finds a key in the database
  def find(self, key):
    if key in self.__database:
      return self.__database[key]
    else:
      raise KeyError("Key not found in database")
  '''

  # A method that returns a list of tuples representing the key-value pairs in the instance variable '__database'
  def items(self):
    return self.__do_to_db('items')

  # A method that returns a list of the keys in the instance variable '__database'
  def keys(self):
    return self.__do_to_db('keys')

  # Removes and returns the value for the given key 'k' from the instance variable '__database'
  def pop(self, k):
    return self.__do_to_db('pop', f"'{k}'")

  # Removes and returns an arbitrary (key, value) pair from the instance variable '__database'
  def popitem(self, k):
    return self.__do_to_db('popitem', f"'{k}'")

  # Returns the value for the given key 'k' from the instance variable '__database'
  def setdefault(self, k):
    return self.__do_to_db('setdefault', f"'{k}'")

  # A method that returns a list of the values in the instance variable '__database'
  def values(self):
    return self.__do_to_db('values')

  # Method that updates the database instance variable with the key-value pairs from a dictionary passed as an argument
  def update(self, other_dict):
    self.__database.update(other_dict)
    self.__save_db()
    self.__update_db()

  def get_path(self):
    return self.__db_location

  # A helper method that updates the instance variable '__database' using the given operation and returns its output
  def __do_to_db(self, operation, arg=None):
    self.__update_db()
    output = eval(f"self._database__database.{operation}({arg})") if arg != None else eval(f"self._database__database.{operation}()")
    self.__save_db()
    return output