import sys
import os
import dropbox
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from logprint import custom_print
class dbf:
  def __init__(self):
    self.dbx = dropbox.Dropbox(
    app_key='x3wr7i2mscrmwgj', 
    app_secret=os.environ['x3wr7i2mscrmwgj'],
    oauth2_refresh_token = os.environ['dropbox_key']
    )

  def download(self, file_path: str, download_path = None) -> None:
    try:
      if file_path[0] != '/': file_path = f"/{file_path}"
      if download_path == None: download_path = file_path[1:]
      _, file = self.dbx.files_download(file_path)
      with open(download_path, 'wb+') as download:
        download.write(file.content)
    except dropbox.exceptions.ApiError:
      custom_print(f"Can't download {file_path}. File does not exist")

  def remove(self, file_path: str) -> None:
    try:
      os.remove(file_path)
    except FileNotFoundError:
      custom_print(f"Can't remove {file_path}. File does not exist")

  def listdir(self, folder_path: str) -> list:
    try:
      if folder_path[0] != '/': folder_path = f"/{folder_path}"
      files = self.dbx.files_list_folder(folder_path)
      output = [file.name for file in files.entries]
      return output
    except dropbox.exceptions.ApiError:
      custom_print(f"Can't list folder {folder_path}. Folder does not exist") 