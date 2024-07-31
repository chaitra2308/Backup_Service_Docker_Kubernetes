import shutil 
from datetime import datetime 

def create_zip(path, file_name):
    # use shutil to create a zip file
    try:
        print("Entered zip")
        shutil.make_archive(f"../archive/{file_name}", 'zip', path)
        print("Zip archive created successfully")
        return True
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False