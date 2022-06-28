#Dockerfile
FROM python:3.9
RUN mkdir /application
RUN mkdir /application/data
RUN mkdir /utils
WORKDIR "/application"
# Upgrade pip
RUN pip install --upgrade pip
# Update
RUN apt-get update \
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*
ADD requirements.txt /application/
ADD main.py /application/
ADD crawl.py /application/
ADD search.py /application/
ADD set_scraping_start.py /application
ADD Scraping2 /application/Scraping2
ADD Scraping2/spiders /application/Scraping2/spiders
ADD utils /application/utils
RUN pip install -r /application/requirements.txt
ENTRYPOINT  [ "python", "main.py" ]

##Dockerfile
#FROM python:3.9
#RUN mkdir /application
#WORKDIR "/application"
## Upgrade pip
#RUN pip install --upgrade pip
## Update
#RUN apt-get update \
#    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*
#ADD requirements.txt /application/
#ADD src/script.py /application/
#RUN pip install -r /application/requirements.txt
#CMD [ "python", "script.py" ]