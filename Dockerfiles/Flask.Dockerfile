FROM python:3.9.2

WORKDIR /online-course-manager

ENV FLASK_APP=flaskr/app
# ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

# upgrade pip
RUN pip install --upgrade pip

# install pip dependencies
RUN pip3 install -r requirements.txt

COPY flaskr .
COPY .env .env

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]