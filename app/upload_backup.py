import os.path

def upload_backup(drive, path, file_name):
    # create a google drive file instance with title metadata
    f = drive.CreateFile({'title': file_name}) 
    # set the path to zip file
    f.SetContentFile(os.path.join(path, file_name)) 
    # start upload
    f.Upload() 
    # set f to none because of a vulnerability found in PyDrive
    f = None