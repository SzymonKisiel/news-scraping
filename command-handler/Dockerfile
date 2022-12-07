# Dockerfile
FROM python:3.9

RUN mkdir /application
WORKDIR /application

# Upgrade pip
RUN pip install --upgrade pip

# Clean up
RUN apt-get -y update \
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

# Add sources
ADD requirements.txt /application/
ADD .env.prod /application/.env
ADD app.py /application/
ADD docker_settings.py /application/settings.py
ADD main.py /application/
ADD settings.py /application/
ADD database /application/database
ADD services /application/services
ADD utils /application/utils

RUN pip install --no-cache-dir -r /application/requirements.txt
RUN pip install gunicorn

EXPOSE 5001

#ENTRYPOINT  [ "python", "main.py" ]
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5001", "--log-level", "debug", "main:app" ]