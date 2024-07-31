#GDrive Backup using Docker & Kubernetes
### Learning Goals

1. Understand API's and how you can use API's to manipulate Cloud Resoucres
2. Understand containerization and how you can package your application to run on any system
3. Understand how you can control orchestrate containers  using Kubernetes

### Deliverables

   1. Using Google's API, write a python script to upload the contents of your folder to Gdrive. 
   2. Containerize your application and all required dependencies and build a Docker image.
   3. Now,using Kubernets, Orchestrate(Control) your application to conduct back ups of your chosen folder at fixed intervals.

### Notes
 1. The main logic of the app is the quickstart.py file, which uses the Google API to list out files on GDrive.

 2. Add credentials.json file with the one you obtain for you Google drive to have acess to the API.

 3.  Modify the Dockerfile appropriately to package your application and required dependencies
 4. Please don't upload your containers publicly onto public registries like DockerHub as sensitive Gdrive data might get leaked.
