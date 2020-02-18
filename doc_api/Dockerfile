##DockerFile
#Pulling base python image from dockerhub
FROM python:3
# Create app directory as working directory
WORKDIR /app
# Copy code from root repo to the working directory
COPY ./requirements.txt /app/
#Run python commands to build and serve the application
RUN pip3 install -r /app/requirements.txt
#Copying nginx conf file to nginx configuration path
#Giving executable permission
COPY . /app/
CMD ["sh", "-c", "python manage.py db upgrade head && waitress-serve --port 5000 manage:app"]
