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

# Download the Chrome Driver and unzip it into /chromedriver directory
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROME_VERSION=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# Set display port as an environment variable (for Google Chrome)
ENV DISPLAY=:99
# Setup IS_DOCKER environment variable
ENV IS_DOCKER Yes

# Add sources
ADD requirements.txt /application/
ADD main.py /application/
ADD console_app /application/console_app
ADD flask_server /application/flask_server
ADD model /application/model
ADD modules /application/modules
ADD news_scraping /application/news_scraping
ADD news_scraping/spiders /application/news_scraping/spiders
ADD settings /application/settings
ADD utils /application/utils

RUN pip install -r /application/requirements.txt
RUN pip install gunicorn

EXPOSE 5002

#ENTRYPOINT  [ "python", "main.py" ]
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5002", "--log-level", "debug", "main:app" ]