#######################################
### Runbook.io - Actions Dockerfile ###
#######################################



# Pull base image
FROM dockerfile/ubuntu

# Update
RUN apt-get update
RUN apt-get upgrade -y

# Install python
#RUN apt-get install -y python python-dev python-pip python-virtualenv wget unzip
RUN apt-get install -y python python-dev python-setuptools build-essential wget unzip
RUN easy_install -U pip
RUN rm -rf /var/lib/apt/lists/*

# Create working directory
RUN mkdir -p /code /config
ADD requirements.txt /config/requirements.txt

# Install requirements
RUN pip install -r /config/requirements.txt

EXPOSE 6000
EXPOSE 6001
