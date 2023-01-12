FROM python:3.9-slim-bullseye

#Build Instructions
WORKDIR /docker-python
COPY requirements.txt requirements.txt
RUN apt-get update -y && apt-get install python3 -y python3-pip
RUN pip3 install -r requirements.txt
COPY . .

ENV FLASK_APP=app.py

#Boot command
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]