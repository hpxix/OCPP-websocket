FROM python:3.11.4-slim-bullseye

RUN apt-get update && apt-get install -y build-essential

RUN mkdir -p /usr/src/csms
WORKDIR /usr/src/csms

COPY ./src /usr/src/csms

#Step3 After Installing websocket watchdog for reload, you'll run through 'core' module not found so 
ENV PYTHONPATH=/usr/src/csms

#STEP 2 AFTER INSTALLING PIP DO THIS 
RUN pip install --no-cache-dir -r /usr/src/csms/requirements.txt

