#Dockerfile
FROM python:3.9
RUN mkdir /application
RUN mkdir /application/data
RUN mkdir /application/data/settings
RUN mkdir /utils
WORKDIR "/application"
# Upgrade pip
RUN pip install --upgrade pip
# Update
RUN apt-get update \
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*
ADD requirements.txt /application/
ADD main.py /application/
ADD modules /application/modules
ADD news_scraping /application/news_scraping
ADD news_scraping/spiders /application/news_scraping/spiders
ADD settings /application/settings
ADD utils /application/utils

#temp
ADD data/settings /application/data/settings

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