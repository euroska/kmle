##DockerFile
#Pulling base python image from dockerhub
FROM python:3
# Create app directory as working directory
WORKDIR /app
# Copy code from root repo to the working directory
COPY . /app
#Run python commands to build and serve the application
RUN pip3 install -r /app/requirements.txt
#Copying nginx conf file to nginx configuration path
#Giving executable permission
CMD ["python", "manage.py", "run"]
