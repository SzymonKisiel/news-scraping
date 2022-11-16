# Dockerfile
FROM python:3.9

RUN mkdir /application
RUN mkdir /application/data
RUN mkdir /application/data/settings
RUN mkdir /utils
WORKDIR "/application"
# Upgrade pip
RUN pip install --upgrade pip
# Add Google Chrome to repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Update
# Install Google Chrome and Unzip
# Clean up
RUN apt-get -y update \
    && apt-get install -y google-chrome-stable \
    && apt-get install -yqq unzip \
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

# Download the Chrome Driver and unzip it into /usr/local/bin directory
RUN wget -N http://chromedriver.storage.googleapis.com/106.0.5249.61/chromedriver_linux64.zip -P /tmp
RUN unzip /tmp/chromedriver_linux64.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99
# Setup IS_DOCKER variable
ENV IS_DOCKER Yes

# Add sources
ADD requirements.txt /application/
ADD main.py /application/
ADD model /application/model
ADD modules /application/modules
ADD news_scraping /application/news_scraping
ADD news_scraping/spiders /application/news_scraping/spiders
ADD settings /application/settings
ADD utils /application/utils

RUN pip install -r /application/requirements.txt
ENTRYPOINT  [ "python", "main.py" ]
