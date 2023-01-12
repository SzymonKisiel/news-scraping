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
ADD app.py /application/
ADD celery_app.py /application/
ADD main.py /application/
ADD database /application/database
ADD models /application/models
ADD services /application/services
ADD utils /application/utils

RUN pip install -r /application/requirements.txt
RUN pip install gunicorn

# Download sentiment models
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained('Voicelab/herbert-base-cased-sentiment'); AutoModelForSequenceClassification.from_pretrained('Voicelab/herbert-base-cased-sentiment')"

# Download sentencizer model
RUN pip install -U pip setuptools wheel
RUN python -m spacy download pl_core_news_md

EXPOSE 5003
# Setup IS_DOCKER environment variable
ENV IS_DOCKER Yes

#ENTRYPOINT  [ "python", "main.py" ]
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5003", "--log-level", "debug", "main:app" ]