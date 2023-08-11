from datetime import datetime

def custom_print(message_to_print, log_file='log.txt'):
  message_to_print = message_to_print.replace('&#x2005;', ' ').replace('^', '').replace('---\n','')
  print(f"{datetime.now().date()} - {datetime.now().time().isoformat(timespec='seconds')}: {message_to_print}\n")
  with open(log_file, 'a') as of:
    of.write(f"{datetime.now().date()} - {datetime.now().time().isoformat(timespec='seconds')}: ")
    of.write(f"{message_to_print}\n")