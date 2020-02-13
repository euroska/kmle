##DockerFile
#Pulling base python image from dockerhub
FROM python:3-alpine
# Create app directory as working directory
WORKDIR /opt/doc_api
# Copy code from root repo to the working directory
COPY . /opt/doc_api
#Run python commands to build and serve the application
RUN pip install /opt/doc_api && rm -rf /opt/doc_api
#Copying nginx conf file to nginx configuration path
#Giving executable permission
CMD [“/usr/bin/python3.6”]
